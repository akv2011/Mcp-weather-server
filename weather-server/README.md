# Weather MCP Server

A Model Context Protocol (MCP) server that provides weather forecast and alert tools using the US National Weather Service API.

## Features

- **get_forecast**: Get weather forecast for any US location using latitude/longitude
- **get_alerts**: Get active weather alerts for any US state using state code

## Quick Start

### Prerequisites

- Python 3.10 or higher
- uv package manager (will be installed automatically if missing)

### Installation

1. Navigate to the weather-server directory:
   ```powershell
   cd weather-server
   ```

2. Run the setup script:
   ```powershell
   python setup.py
   ```

3. Or install manually:
   ```powershell
   # Install uv if not present
   powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
   
   # Create virtual environment and install dependencies
   uv venv
   uv add mcp httpx
   ```

### Running the Server

```powershell
uv run weather.py
```

## Configuration with Claude Desktop

Add this configuration to your Claude Desktop config file (`%AppData%\Claude\claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "weather": {
      "command": "uv",
      "args": [
        "--directory",
        "C:\\ABSOLUTE\\PATH\\TO\\weather-server",
        "run",
        "weather.py"
      ]
    }
  }
}
```

Replace `C:\\ABSOLUTE\\PATH\\TO\\weather-server` with the actual absolute path to your weather-server directory.

## Usage Examples

Once configured with Claude Desktop, you can ask:

- "What's the weather forecast for Sacramento, CA?"
- "Are there any weather alerts in Texas?"
- "Show me the forecast for latitude 40.7128, longitude -74.0060"

## API Details

### get_forecast(latitude: float, longitude: float)

Gets a 5-period weather forecast for the specified coordinates.

**Parameters:**
- `latitude`: Latitude of the location
- `longitude`: Longitude of the location

**Returns:** Formatted weather forecast string

### get_alerts(state: str)

Gets active weather alerts for a US state.

**Parameters:**
- `state`: Two-letter US state code (e.g., "CA", "NY", "TX")

**Returns:** Formatted weather alerts string

## Technical Details

- Uses the US National Weather Service API
- Implements proper error handling and timeouts
- Follows MCP protocol specifications
- Uses FastMCP for simplified server development

## Troubleshooting

### Server not showing up in Claude Desktop

1. Check that the path in `claude_desktop_config.json` is correct and absolute
2. Restart Claude Desktop after configuration changes
3. Verify the server runs without errors: `uv run weather.py`

### Weather data not available

- The server only works with US locations (National Weather Service limitation)
- Coordinates must be within the US territory
- State codes must be valid two-letter US state abbreviations

### Common Issues

- **Path issues on Windows**: Use double backslashes (`\\`) or forward slashes (`/`) in JSON paths
- **uv not found**: Make sure to restart your terminal after installing uv
- **Permission errors**: Run PowerShell as administrator if needed for uv installation

## Development

The server is built using:
- **FastMCP**: Simplified MCP server framework
- **httpx**: Async HTTP client for API requests
- **Python 3.10+**: Modern Python features and type hints

To modify or extend the server, edit `weather.py` and restart the server.
