#!/bin/bash
# RSJ-FFMPEG Power Toolkit Installer
# Universal installer for Linux/Mac/Termux
# © 2025 RAJSARASWATI JATAV

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Banner
echo -e "${CYAN}"
cat << "EOF"
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
EOF
echo -e "${NC}"

echo -e "${GREEN}[►] RSJ-FFMPEG Installer v2.0.0${NC}\n"

# Detect platform
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    if [ -n "$TERMUX_VERSION" ]; then
        PLATFORM="termux"
    else
        PLATFORM="linux"
    fi
elif [[ "$OSTYPE" == "darwin"* ]]; then
    PLATFORM="macos"
else
    echo -e "${RED}❌ Unsupported platform: $OSTYPE${NC}"
    exit 1
fi

echo -e "${BLUE}[►] Detected platform: $PLATFORM${NC}"

# Check Python
echo -e "${BLUE}[►] Checking Python...${NC}"
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 is not installed${NC}"
    echo -e "${YELLOW}Installing Python...${NC}"
    
    if [ "$PLATFORM" == "termux" ]; then
        pkg install python -y
    elif [ "$PLATFORM" == "linux" ]; then
        sudo apt-get update && sudo apt-get install python3 python3-pip -y
    elif [ "$PLATFORM" == "macos" ]; then
        brew install python3
    fi
fi

PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
echo -e "${GREEN}✅ Python $PYTHON_VERSION${NC}"

# Check FFmpeg
echo -e "${BLUE}[►] Checking FFmpeg...${NC}"
if ! command -v ffmpeg &> /dev/null; then
    echo -e "${YELLOW}⚠️  FFmpeg not found. Installing...${NC}"
    
    if [ "$PLATFORM" == "termux" ]; then
        pkg install ffmpeg -y
    elif [ "$PLATFORM" == "linux" ]; then
        sudo apt-get update && sudo apt-get install ffmpeg -y
    elif [ "$PLATFORM" == "macos" ]; then
        brew install ffmpeg
    fi
else
    echo -e "${GREEN}✅ FFmpeg installed${NC}"
fi

# Install Python dependencies
echo -e "${BLUE}[►] Installing Python dependencies...${NC}"
pip3 install -r requirements.txt

# Install package
echo -e "${BLUE}[►] Installing RSJ-FFMPEG...${NC}"
pip3 install -e .

# Create directory structure
echo -e "${BLUE}[►] Creating directory structure...${NC}"
mkdir -p input output logs reports temp plugins templates assets

# Create symlink for easy access
if [ "$PLATFORM" != "termux" ]; then
    echo -e "${BLUE}[►] Creating command symlink...${NC}"
    sudo ln -sf $(pwd)/cli.py /usr/local/bin/rsj-ffmpeg
    sudo chmod +x /usr/local/bin/rsj-ffmpeg
else
    ln -sf $(pwd)/cli.py $PREFIX/bin/rsj-ffmpeg
    chmod +x $PREFIX/bin/rsj-ffmpeg
fi

# Verify installation
echo -e "\n${BLUE}[►] Verifying installation...${NC}"
if command -v rsj-ffmpeg &> /dev/null; then
    echo -e "${GREEN}✅ RSJ-FFMPEG installed successfully!${NC}"
else
    echo -e "${YELLOW}⚠️  Command not found in PATH. You can run: python3 cli.py${NC}"
fi

# Final message
echo -e "\n${CYAN}╔══════════════════════════════════════════════════════════════╗${NC}"
echo -e "${CYAN}║  ✅ Installation Complete!                                   ║${NC}"
echo -e "${CYAN}║                                                              ║${NC}"
echo -e "${CYAN}║  Get started:                                                ║${NC}"
echo -e "${CYAN}║  $ rsj-ffmpeg --help                                         ║${NC}"
echo -e "${CYAN}║  $ rsj-ffmpeg --system-check                                 ║${NC}"
echo -e "${CYAN}║                                                              ║${NC}"
echo -e "${CYAN}║  Examples:                                                   ║${NC}"
echo -e "${CYAN}║  $ rsj-ffmpeg --batch ./videos/ --export ./output/           ║${NC}"
echo -e "${CYAN}║  $ rsj-ffmpeg -i video.mp4 --ai-upscale 4x -o out.mp4       ║${NC}"
echo -e "${CYAN}║                                                              ║${NC}"
echo -e "${CYAN}║  © 2025 RAJSARASWATI JATAV | All Rights Reserved            ║${NC}"
echo -e "${CYAN}╚══════════════════════════════════════════════════════════════╝${NC}\n"

echo -e "${GREEN}🟢 STAY POWERFUL. STAY CREATIVE. UPGRADE YOURSELF! 🟢${NC}\n"