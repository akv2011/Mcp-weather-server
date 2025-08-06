#!/usr/bin/env python3
"""
Setup script for Puch MCP Server
"""

import subprocess
import sys
import os
from pathlib import Path

def run_command(command, description):
    """Run a command and handle errors."""
    print(f"\n📦 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed")
        print(f"Error: {e.stderr}")
        return None

def main():
    print("🚀 Setting up Puch MCP Server")
    print("=" * 50)
    
    # Install dependencies
    run_command(
        "pip install -r puch_requirements.txt",
        "Installing required packages"
    )
    
    print("\n📋 Setup Instructions:")
    print("1. Get your application key by running: /apply <TWITTER/LINKEDIN REPLY URL>")
    print("2. Edit puch_server.py and replace:")
    print("   - TOKEN = '<generated_token>' with your actual application key")
    print("   - MY_NUMBER = '91XXXXXXXXXX' with your phone number (format: {country_code}{number})")
    print("3. Place your resume file (PDF, DOCX, TXT, or MD) in this directory")
    print("   - File should contain 'resume' or 'cv' in the name")
    print("4. Run the server: python puch_server.py")
    print("5. Connect Puch with: /mcp connect <SERVER URL>/mcp <AUTH TOKEN>")
    
    print("\n📁 Current directory contents:")
    current_dir = Path.cwd()
    for file in current_dir.iterdir():
        if file.is_file():
            print(f"   - {file.name}")
    
    print("\n🔧 To start the server after configuration:")
    print("   python puch_server.py")

if __name__ == "__main__":
    main()
