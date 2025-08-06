# Puch AI Clone - MCP Server Collection

A collection of Model Context Protocol (MCP) servers for extending AI assistant capabilities.

## 🌤️ Weather MCP Server

A weather forecasting server that provides:
- **Weather forecasts** for any US location (using latitude/longitude)
- **Weather alerts** for US states (using state codes)

### Quick Setup

1. **Easy setup** (Windows):
   ```cmd
   setup-weather.bat
   ```

2. **Manual setup**:
   ```powershell
   cd weather-server
   powershell -ExecutionPolicy Bypass -File setup.ps1
   ```

3. **Test the server**:
   ```powershell
   powershell -File test-weather-server.ps1
   ```

### Usage with Claude Desktop

The weather server is automatically configured in your MCP settings. After setup:

1. Restart Claude Desktop
2. Look for the weather tools in the tool selector
3. Ask questions like:
   - "What's the weather forecast for Sacramento?"
   - "Are there any weather alerts in Texas?"

## 🔧 Other MCP Servers

- **task-master-ai**: AI-powered task management (pre-configured)

## 📁 Project Structure

```
Puch_ai_clone/
├── weather-server/          # Weather MCP server
│   ├── weather.py          # Main server implementation
│   ├── setup.ps1           # Windows setup script
│   └── README.md           # Weather server documentation
├── .vscode/
│   └── mcp.json            # MCP server configurations
├── setup-weather.bat       # Quick weather setup
├── test-weather-server.ps1 # Test script
└── README.md               # This file
```

## 🚀 Getting Started

1. Clone this repository
2. Run the weather server setup: `setup-weather.bat`
3. Configure Claude Desktop (done automatically)
4. Start using the weather tools!

## 🛠️ Development

Each MCP server is self-contained in its own directory with:
- Implementation files
- Setup scripts
- Documentation
- Dependencies

To add new servers, create a new directory and follow the MCP server development guidelines.

## 📖 Learn More

- [MCP Documentation](https://modelcontextprotocol.io/)
- [Weather Server Details](weather-server/README.md)
- [MCP Server Development Tutorial](https://modelcontextprotocol.io/docs/tutorials/server-development)

## 🤝 Contributing

Feel free to add new MCP servers or improve existing ones!