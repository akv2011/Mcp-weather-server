from typing import Annotated
from fastmcp import FastMCP
from fastmcp.server.auth.providers.bearer import BearerAuthProvider, RSAKeyPair
import markdownify
from mcp import ErrorData, McpError
from mcp.server.auth.provider import AccessToken
from mcp.types import INTERNAL_ERROR, INVALID_PARAMS, TextContent
from pydantic import BaseModel, AnyUrl, Field
import readabilipy
from pathlib import Path
import os
import docx2txt
import PyPDF2
from io import BytesIO

# Application key from Puch
TOKEN = "1557ae62b96f"
MY_NUMBER = "919360011424"  # +91 9360011424 formatted as {country_code}{number}


class RichToolDescription(BaseModel):
    description: str
    use_when: str
    side_effects: str | None


class SimpleBearerAuthProvider(BearerAuthProvider):
    """
    A simple BearerAuthProvider that does not require any specific configuration.
    It allows any valid bearer token to access the MCP server.
    For a more complete implementation that can authenticate dynamically generated tokens,
    please use `BearerAuthProvider` with your public key or JWKS URI.
    """

    def __init__(self, token: str):
        k = RSAKeyPair.generate()
        super().__init__(
            public_key=k.public_key, jwks_uri=None, issuer=None, audience=None
        )
        self.token = token

    async def load_access_token(self, token: str) -> AccessToken | None:
        if token == self.token:
            return AccessToken(
                token=token,
                client_id="unknown",
                scopes=[],
                expires_at=None,  # No expiration for simplicity
            )
        return None


class Fetch:
    IGNORE_ROBOTS_TXT = True
    USER_AGENT = "Puch/1.0 (Autonomous)"

    @classmethod
    async def fetch_url(
        cls,
        url: str,
        user_agent: str,
        force_raw: bool = False,
    ) -> tuple[str, str]:
        """
        Fetch the URL and return the content in a form ready for the LLM, as well as a prefix string with status information.
        """
        from httpx import AsyncClient, HTTPError

        async with AsyncClient() as client:
            try:
                response = await client.get(
                    url,
                    follow_redirects=True,
                    headers={"User-Agent": user_agent},
                    timeout=30,
                )
            except HTTPError as e:
                raise McpError(
                    ErrorData(
                        code=INTERNAL_ERROR, message=f"Failed to fetch {url}: {e!r}"
                    )
                )
            if response.status_code >= 400:
                raise McpError(
                    ErrorData(
                        code=INTERNAL_ERROR,
                        message=f"Failed to fetch {url} - status code {response.status_code}",
                    )
                )

            page_raw = response.text

        content_type = response.headers.get("content-type", "")
        is_page_html = (
            "<html" in page_raw[:100] or "text/html" in content_type or not content_type
        )

        if is_page_html and not force_raw:
            return cls.extract_content_from_html(page_raw), ""

        return (
            page_raw,
            f"Content type {content_type} cannot be simplified to markdown, but here is the raw content:\n",
        )

    @staticmethod
    def extract_content_from_html(html: str) -> str:
        """Extract and convert HTML content to Markdown format.

        Args:
            html: Raw HTML content to process

        Returns:
            Simplified markdown version of the content
        """
        ret = readabilipy.simple_json.simple_json_from_html_string(
            html, use_readability=True
        )
        if not ret["content"]:
            return "<error>Page failed to be simplified from HTML</error>"
        content = markdownify.markdownify(
            ret["content"],
            heading_style=markdownify.ATX,
        )
        return content


class ResumeProcessor:
    """Handle resume file processing and conversion to markdown."""
    
    @staticmethod
    def read_pdf(file_path: str) -> str:
        """Extract text from PDF file."""
        try:
            with open(file_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                text = ""
                for page in reader.pages:
                    text += page.extract_text() + "\n"
                return text.strip()
        except Exception as e:
            raise McpError(
                ErrorData(code=INTERNAL_ERROR, message=f"Failed to read PDF: {e}")
            )

    @staticmethod
    def read_docx(file_path: str) -> str:
        """Extract text from DOCX file."""
        try:
            return docx2txt.process(file_path)
        except Exception as e:
            raise McpError(
                ErrorData(code=INTERNAL_ERROR, message=f"Failed to read DOCX: {e}")
            )

    @staticmethod
    def read_txt(file_path: str) -> str:
        """Read text from TXT file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()
        except Exception as e:
            raise McpError(
                ErrorData(code=INTERNAL_ERROR, message=f"Failed to read TXT: {e}")
            )

    @staticmethod
    def text_to_markdown(text: str) -> str:
        """Convert plain text to basic markdown format."""
        lines = text.split('\n')
        markdown_lines = []
        
        for line in lines:
            line = line.strip()
            if not line:
                markdown_lines.append("")
                continue
                
            # Convert common resume sections to headers
            if any(keyword in line.upper() for keyword in [
                'EXPERIENCE', 'EDUCATION', 'SKILLS', 'PROJECTS', 
                'CONTACT', 'SUMMARY', 'OBJECTIVE', 'ACHIEVEMENTS',
                'CERTIFICATIONS', 'PUBLICATIONS', 'AWARDS'
            ]):
                markdown_lines.append(f"## {line}")
            # Convert bullet points
            elif line.startswith('•') or line.startswith('-') or line.startswith('*'):
                markdown_lines.append(f"- {line[1:].strip()}")
            else:
                markdown_lines.append(line)
        
        return '\n'.join(markdown_lines)

    @classmethod
    def find_resume_file(cls) -> str:
        """Find resume file in common locations."""
        current_dir = Path.cwd()
        resume_patterns = [
            "resume.*",
            "cv.*",
            "*resume*",
            "*cv*"
        ]
        
        for pattern in resume_patterns:
            for file_path in current_dir.glob(pattern):
                if file_path.is_file() and file_path.suffix.lower() in ['.pdf', '.docx', '.txt', '.md']:
                    return str(file_path)
        
        # Check parent directories
        parent_dir = current_dir.parent
        for pattern in resume_patterns:
            for file_path in parent_dir.glob(pattern):
                if file_path.is_file() and file_path.suffix.lower() in ['.pdf', '.docx', '.txt', '.md']:
                    return str(file_path)
        
        raise McpError(
            ErrorData(
                code=INTERNAL_ERROR, 
                message="Resume file not found. Please place your resume (PDF, DOCX, TXT, or MD) in the current directory with 'resume' or 'cv' in the filename."
            )
        )

    @classmethod
    def process_resume(cls, file_path: str = None) -> str:
        """Process resume file and return as markdown."""
        if not file_path:
            file_path = cls.find_resume_file()
        
        if not os.path.exists(file_path):
            raise McpError(
                ErrorData(code=INTERNAL_ERROR, message=f"Resume file not found: {file_path}")
            )
        
        file_ext = Path(file_path).suffix.lower()
        
        if file_ext == '.pdf':
            text = cls.read_pdf(file_path)
        elif file_ext == '.docx':
            text = cls.read_docx(file_path)
        elif file_ext in ['.txt', '.md']:
            text = cls.read_txt(file_path)
        else:
            raise McpError(
                ErrorData(
                    code=INVALID_PARAMS, 
                    message=f"Unsupported file format: {file_ext}. Supported formats: PDF, DOCX, TXT, MD"
                )
            )
        
        if file_ext == '.md':
            return text  # Already in markdown format
        else:
            return cls.text_to_markdown(text)


mcp = FastMCP(
    "Puch MCP Server",
    auth=SimpleBearerAuthProvider(TOKEN),
)

ResumeToolDescription = RichToolDescription(
    description="Serve your resume in plain markdown.",
    use_when="Puch (or anyone) asks for your resume; this must return raw markdown, no extra formatting.",
    side_effects=None,
)

@mcp.tool(description=ResumeToolDescription.model_dump_json())
async def resume() -> str:
    """
    Return your resume exactly as markdown text.
    
    This function:
    1. Accepts a local file (your resume PDF)
    2. Converts it to markdown text
    3. Returns the resume as markdown text
    """
    try:
        # Process the PDF resume file from Downloads
        resume_markdown = ResumeProcessor.process_resume('C:\\Users\\arunk\\Downloads\\Resume_._.arun.pdf')
        return resume_markdown
    except Exception as e:
        # Fallback to the pre-formatted markdown if PDF processing fails
        try:
            with open('arunkumar_resume.md', 'r', encoding='utf-8') as f:
                resume_markdown = f.read()
            return resume_markdown
        except Exception as fallback_error:
            raise McpError(
                ErrorData(code=INTERNAL_ERROR, message=f"Failed to process resume: {e}. Fallback also failed: {fallback_error}")
            )


@mcp.tool
async def validate() -> str:
    """
    NOTE: This tool must be present in an MCP server used by puch.
    Returns the phone number for validation.
    """
    return MY_NUMBER


FetchToolDescription = RichToolDescription(
    description="Fetch a URL and return its content.",
    use_when="Use this tool when the user provides a URL and asks for its content, or when the user wants to fetch a webpage.",
    side_effects="The user will receive the content of the requested URL in a simplified format, or raw HTML if requested.",
)


@mcp.tool(description=FetchToolDescription.model_dump_json())
async def fetch(
    url: Annotated[AnyUrl, Field(description="URL to fetch")],
    max_length: Annotated[
        int,
        Field(
            default=5000,
            description="Maximum number of characters to return.",
            gt=0,
            lt=1000000,
        ),
    ] = 5000,
    start_index: Annotated[
        int,
        Field(
            default=0,
            description="On return output starting at this character index, useful if a previous fetch was truncated and more context is required.",
            ge=0,
        ),
    ] = 0,
    raw: Annotated[
        bool,
        Field(
            default=False,
            description="Get the actual HTML content if the requested page, without simplification.",
        ),
    ] = False,
) -> list[TextContent]:
    """Fetch a URL and return its content."""
    url_str = str(url).strip()
    if not url:
        raise McpError(ErrorData(code=INVALID_PARAMS, message="URL is required"))

    content, prefix = await Fetch.fetch_url(url_str, Fetch.USER_AGENT, force_raw=raw)
    original_length = len(content)
    if start_index >= original_length:
        content = "<error>No more content available.</error>"
    else:
        truncated_content = content[start_index : start_index + max_length]
        if not truncated_content:
            content = "<error>No more content available.</error>"
        else:
            content = truncated_content
            actual_content_length = len(truncated_content)
            remaining_content = original_length - (start_index + actual_content_length)
            # Only add the prompt to continue fetching if there is still remaining content
            if actual_content_length == max_length and remaining_content > 0:
                next_start = start_index + actual_content_length
                content += f"\n\n<error>Content truncated. Call the fetch tool with a start_index of {next_start} to get more content.</error>"
    return [TextContent(type="text", text=f"{prefix}Contents of {url}:\n{content}")]


async def main():
    print("Starting Puch MCP Server...")
    print(f"Server will be available at: http://0.0.0.0:8085")
    print(f"Auth token: {TOKEN}")
    print(f"Phone number for validation: {MY_NUMBER}")
    await mcp.run_async(
        "streamable-http",
        host="0.0.0.0",
        port=8085,
    )


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
