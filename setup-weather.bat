@echo off
echo 🌤️  Weather MCP Server Quick Setup
echo ================================

cd weather-server
if not exist weather.py (
    echo ❌ Weather server files not found
    pause
    exit /b 1
)

echo Running PowerShell setup script...
powershell -ExecutionPolicy Bypass -File setup.ps1

echo.
echo Setup complete! Press any key to continue...
pause >nul
