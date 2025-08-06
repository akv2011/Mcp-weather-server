# Puch MCP Server Launcher
# PowerShell script to set up and run the Puch MCP server

Write-Host "🚀 Puch MCP Server Launcher" -ForegroundColor Green
Write-Host "================================" -ForegroundColor Green

# Check if Python is installed
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✅ Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Python not found. Please install Python first." -ForegroundColor Red
    exit 1
}

# Check if puch_server.py exists
if (-not (Test-Path "puch_server.py")) {
    Write-Host "❌ puch_server.py not found in current directory" -ForegroundColor Red
    exit 1
}

# Check if requirements file exists
if (Test-Path "puch_requirements.txt") {
    Write-Host "📦 Installing dependencies..." -ForegroundColor Yellow
    pip install -r puch_requirements.txt
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Dependencies installed successfully" -ForegroundColor Green
    } else {
        Write-Host "❌ Failed to install dependencies" -ForegroundColor Red
        exit 1
    }
} else {
    Write-Host "⚠️  puch_requirements.txt not found, skipping dependency installation" -ForegroundColor Yellow
}

# Check for resume file
$resumeFound = $false
$resumeFiles = @("resume.pdf", "resume.docx", "resume.txt", "resume.md", "cv.pdf", "cv.docx", "cv.txt", "cv.md")

foreach ($file in $resumeFiles) {
    if (Test-Path $file) {
        Write-Host "✅ Resume file found: $file" -ForegroundColor Green
        $resumeFound = $true
        break
    }
}

if (-not $resumeFound) {
    Write-Host "⚠️  No resume file found. Please add your resume with 'resume' or 'cv' in the filename." -ForegroundColor Yellow
    Write-Host "   Supported formats: PDF, DOCX, TXT, MD" -ForegroundColor Yellow
}

# Check if server is configured
$serverContent = Get-Content "puch_server.py" -Raw
if ($serverContent -like "*<generated_token>*" -or $serverContent -like "*91XXXXXXXXXX*") {
    Write-Host "" -ForegroundColor Yellow
    Write-Host "⚠️  CONFIGURATION REQUIRED:" -ForegroundColor Yellow
    Write-Host "   1. Get your application key: /apply <TWITTER/LINKEDIN REPLY URL>" -ForegroundColor Yellow
    Write-Host "   2. Edit puch_server.py and replace:" -ForegroundColor Yellow
    Write-Host "      - TOKEN = '<generated_token>' with your actual key" -ForegroundColor Yellow
    Write-Host "      - MY_NUMBER = '91XXXXXXXXXX' with your phone number" -ForegroundColor Yellow
    Write-Host ""
    
    $continue = Read-Host "Continue anyway? (y/N)"
    if ($continue -ne "y" -and $continue -ne "Y") {
        Write-Host "Setup cancelled. Please configure the server first." -ForegroundColor Yellow
        exit 0
    }
}

Write-Host ""
Write-Host "🚀 Starting Puch MCP Server..." -ForegroundColor Green
Write-Host "   Server URL: http://localhost:8085" -ForegroundColor Cyan
Write-Host "   Press Ctrl+C to stop the server" -ForegroundColor Yellow
Write-Host ""

# Start the server
try {
    python puch_server.py
} catch {
    Write-Host "❌ Failed to start server" -ForegroundColor Red
    exit 1
}
