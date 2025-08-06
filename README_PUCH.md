# Puch MCP Server

This is an MCP (Model Context Protocol) server implementation for the Puch application process. The server provides tools for resume processing, URL fetching, and validation.

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r puch_requirements.txt
```

Or run the setup script:
```bash
python setup_puch.py
```

### 2. Configuration

Before running the server, you need to configure two important values in `puch_server.py`:

#### Get Your Application Key
1. Run the command: `/apply <TWITTER/LINKEDIN REPLY URL>`
2. You'll receive an application key
3. Replace `TOKEN = "<generated_token>"` with your actual key

#### Set Your Phone Number
Replace `MY_NUMBER = "91XXXXXXXXXX"` with your phone number in the format `{country_code}{number}` (without the + symbol).

**Examples:**
- Indian number: `919876543210`
- US number: `15551234567`
- UK number: `447912345678`

### 3. Add Your Resume

Place your resume file in the project directory with one of these formats:
- **PDF**: `resume.pdf`, `cv.pdf`, `my_resume.pdf`
- **DOCX**: `resume.docx`, `cv.docx`, `my_resume.docx`
- **TXT**: `resume.txt`, `cv.txt`, `my_resume.txt`
- **Markdown**: `resume.md`, `cv.md`, `my_resume.md`

The server automatically finds files containing "resume" or "cv" in the filename.

### 4. Run the Server

```bash
python puch_server.py
```

The server will start on `http://0.0.0.0:8085`

### 5. Connect with Puch

Use this command to connect Puch with your MCP server:
```
/mcp connect <SERVER URL>/mcp <AUTH TOKEN>
```

Where:
- `<SERVER URL>` is your publicly accessible server URL
- `<AUTH TOKEN>` is the application key you received

## 🛠 Server Features

### Resume Tool
- **Purpose**: Serves your resume in markdown format
- **Functionality**: 
  - Automatically finds resume files in the directory
  - Supports PDF, DOCX, TXT, and Markdown formats
  - Converts content to clean markdown
  - Handles common resume sections (Experience, Education, Skills, etc.)

### Validate Tool
- **Purpose**: Validates your phone number for Puch authentication
- **Returns**: Your configured phone number for validation

### Fetch Tool
- **Purpose**: Fetches web content and converts to markdown
- **Features**:
  - URL content fetching
  - HTML to markdown conversion
  - Content truncation and pagination
  - Raw HTML option

## 📁 File Structure

```
├── puch_server.py           # Main MCP server implementation
├── puch_requirements.txt    # Python dependencies
├── setup_puch.py           # Setup and installation script
├── README_PUCH.md          # This documentation
└── resume.pdf              # Your resume file (add this)
```

## 🔧 Troubleshooting

### Resume Not Found
- Ensure your resume file contains "resume" or "cv" in the filename
- Supported formats: PDF, DOCX, TXT, MD
- File should be in the same directory as `puch_server.py`

### Authentication Issues
- Verify your TOKEN is correctly set in `puch_server.py`
- Check that MY_NUMBER follows the correct format: `{country_code}{number}`
- No spaces, dashes, or + symbols in the phone number

### Server Connection Issues
- Ensure the server is running on port 8085
- Check that your server URL is publicly accessible
- Verify firewall settings allow connections on port 8085

### Dependencies
If you encounter import errors, install dependencies manually:
```bash
pip install fastmcp markdownify readabilipy pydantic httpx PyPDF2 python-docx docx2txt
```

## 📋 Validation Requirements

Puch will validate:
1. **Auth Token**: Must match the application key you received
2. **Phone Number**: Must be formatted correctly and match your actual number
3. **Resume Tool**: Must return valid markdown content
4. **Server Accessibility**: Must be publicly accessible via the provided URL

## 🔒 Security Notes

- Keep your application token secure
- Don't commit tokens to version control
- Ensure your server is properly configured for public access
- Consider using environment variables for sensitive data

## 📞 Support

If you encounter issues:
1. Check the console output for error messages
2. Verify all configuration steps are completed
3. Test resume file processing locally
4. Ensure network connectivity and firewall settings

---

**Important**: Replace placeholder values in `puch_server.py` before running the server!
