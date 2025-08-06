# Test script for the Weather MCP Server
# This script tests the weather server functionality

Write-Host "🧪 Testing Weather MCP Server" -ForegroundColor Cyan
Write-Host "=" * 40

$weatherServerPath = "weather-server"

# Check if the weather server directory exists
if (-not (Test-Path $weatherServerPath)) {
    Write-Host "❌ Weather server directory not found at: $weatherServerPath" -ForegroundColor Red
    exit 1
}

# Change to weather server directory
Push-Location $weatherServerPath

try {
    # Check if the weather.py file exists
    if (-not (Test-Path "weather.py")) {
        Write-Host "❌ weather.py not found in weather-server directory" -ForegroundColor Red
        exit 1
    }

    # Check if uv is available
    try {
        $uvVersion = uv --version 2>$null
        Write-Host "✅ uv found: $uvVersion" -ForegroundColor Green
    }
    catch {
        Write-Host "❌ uv not found. Please run setup.ps1 first." -ForegroundColor Red
        exit 1
    }

    # Test server syntax
    Write-Host "Testing server syntax..." -ForegroundColor Yellow
    $syntaxTest = uv run python -m py_compile weather.py 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Server syntax is valid" -ForegroundColor Green
    }
    else {
        Write-Host "❌ Server syntax error:" -ForegroundColor Red
        Write-Host $syntaxTest -ForegroundColor Red
        exit 1
    }

    # Check dependencies
    Write-Host "Checking dependencies..." -ForegroundColor Yellow
    $depsCheck = uv run python -c "import mcp.server.fastmcp; import httpx; print('Dependencies OK')" 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ All dependencies are installed" -ForegroundColor Green
    }
    else {
        Write-Host "❌ Dependencies missing:" -ForegroundColor Red
        Write-Host $depsCheck -ForegroundColor Red
        Write-Host "Run 'uv add mcp httpx' to install dependencies" -ForegroundColor Yellow
        exit 1
    }

    Write-Host ""
    Write-Host "🎉 Weather MCP Server is ready!" -ForegroundColor Green
    Write-Host ""
    Write-Host "To start the server:" -ForegroundColor Cyan
    Write-Host "  cd weather-server" -ForegroundColor White
    Write-Host "  uv run weather.py" -ForegroundColor White
    Write-Host ""
    Write-Host "Configuration for Claude Desktop:" -ForegroundColor Cyan
    Write-Host @"
{
  "mcpServers": {
    "weather": {
      "command": "uv",
      "args": [
        "--directory",
        "$((Get-Location).Path)",
        "run",
        "weather.py"
      ]
    }
  }
}
"@ -ForegroundColor White

}
finally {
    # Return to original directory
    Pop-Location
}

Write-Host ""
Write-Host "📋 Next steps:" -ForegroundColor Cyan
Write-Host "1. Add the configuration above to %AppData%\Claude\claude_desktop_config.json" -ForegroundColor White
Write-Host "2. Restart Claude Desktop" -ForegroundColor White
Write-Host "3. Look for the weather tools in Claude's tool selector" -ForegroundColor White
