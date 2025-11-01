# RSJ-FFMPEG Power Toolkit Installer for Windows
# PowerShell installation script
# © 2025 RAJSARASWATI JATAV

Write-Host @"
╔══════════════════════════════════════════════════════════════╗
║  ██████╗ ███████╗     ██╗    ███████╗███████╗███╗   ███╗    ║
║  ██╔══██╗██╔════╝     ██║    ██╔════╝██╔════╝████╗ ████║    ║
║  ██████╔╝███████╗     ██║    █████╗  █████╗  ██╔████╔██║    ║
║  ██╔══██╗╚════██║██   ██║    ██╔══╝  ██╔══╝  ██║╚██╔╝██║    ║
║  ██║  ██║███████║╚█████╔╝    ██║     ██║     ██║ ╚═╝ ██║    ║
║  ╚═╝  ╚═╝╚══════╝ ╚════╝     ╚═╝     ╚═╝     ╚═╝     ╚═╝    ║
║                                                              ║
║  🔥 ULTIMATE AI-POWERED MULTIMEDIA AUTOMATION FRAMEWORK 🔥   ║
║  By RAJSARASWATI JATAV | Next-Level Power                   ║
╚══════════════════════════════════════════════════════════════╝
"@ -ForegroundColor Cyan

Write-Host "`n[►] RSJ-FFMPEG Installer v2.0.0`n" -ForegroundColor Green

# Check Python
Write-Host "[►] Checking Python..." -ForegroundColor Blue
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✅ $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Python is not installed" -ForegroundColor Red
    Write-Host "Please install Python from: https://www.python.org/downloads/" -ForegroundColor Yellow
    exit 1
}

# Check FFmpeg
Write-Host "[►] Checking FFmpeg..." -ForegroundColor Blue
try {
    $ffmpegVersion = ffmpeg -version 2>&1 | Select-Object -First 1
    Write-Host "✅ FFmpeg installed" -ForegroundColor Green
} catch {
    Write-Host "⚠️  FFmpeg not found" -ForegroundColor Yellow
    Write-Host "Please install FFmpeg from: https://ffmpeg.org/download.html" -ForegroundColor Yellow
    Write-Host "Or use: winget install FFmpeg" -ForegroundColor Yellow
}

# Install Python dependencies
Write-Host "`n[►] Installing Python dependencies..." -ForegroundColor Blue
pip install -r requirements.txt

# Install package
Write-Host "[►] Installing RSJ-FFMPEG..." -ForegroundColor Blue
pip install -e .

# Create directory structure
Write-Host "[►] Creating directory structure..." -ForegroundColor Blue
$directories = @("input", "output", "logs", "reports", "temp", "plugins", "templates", "assets")
foreach ($dir in $directories) {
    New-Item -ItemType Directory -Force -Path $dir | Out-Null
}

# Create batch file for easy access
Write-Host "[►] Creating command shortcut..." -ForegroundColor Blue
$batchContent = @"
@echo off
python "%~dp0cli.py" %*
"@
Set-Content -Path "rsj-ffmpeg.bat" -Value $batchContent

# Add to PATH (optional)
$currentPath = [Environment]::GetEnvironmentVariable("Path", "User")
$scriptPath = (Get-Location).Path
if ($currentPath -notlike "*$scriptPath*") {
    Write-Host "[►] Adding to PATH..." -ForegroundColor Blue
    [Environment]::SetEnvironmentVariable("Path", "$currentPath;$scriptPath", "User")
    Write-Host "✅ Added to PATH (restart terminal to use 'rsj-ffmpeg' command)" -ForegroundColor Green
}

# Final message
Write-Host @"

╔══════════════════════════════════════════════════════════════╗
║  ✅ Installation Complete!                                   ║
║                                                              ║
║  Get started:                                                ║
║  > rsj-ffmpeg --help                                         ║
║  > rsj-ffmpeg --system-check                                 ║
║                                                              ║
║  Examples:                                                   ║
║  > rsj-ffmpeg --batch .\videos\ --export .\output\           ║
║  > rsj-ffmpeg -i video.mp4 --ai-upscale 4x -o out.mp4       ║
║                                                              ║
║  © 2025 RAJSARASWATI JATAV | All Rights Reserved            ║
╚══════════════════════════════════════════════════════════════╝

"@ -ForegroundColor Cyan

Write-Host "🟢 STAY POWERFUL. STAY CREATIVE. UPGRADE YOURSELF! 🟢`n" -ForegroundColor Green