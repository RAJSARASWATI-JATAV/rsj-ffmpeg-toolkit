# 🔥 RSJ-FFMPEG TOOLKIT - COMPLETE INSTALLATION GUIDE

**Author:** RAJSARASWATI JATAV  
**Version:** 2.2.0  
**Status:** Production Ready

---

## 📋 PREREQUISITES

### Required Software
1. **Python 3.8+** - [Download](https://www.python.org/downloads/)
2. **FFmpeg** - [Download](https://ffmpeg.org/download.html)
3. **Git** (optional) - [Download](https://git-scm.com/downloads/)

### Verify Installation
```bash
python --version    # Should be 3.8 or higher
ffmpeg -version     # Should show FFmpeg version
```

---

## 🚀 INSTALLATION METHODS

### Method 1: Quick Install (Recommended)

#### Windows (PowerShell)
```powershell
# Clone repository
git clone https://github.com/RAJSARASWATI-JATAV/rsj-ffmpeg-toolkit.git
cd rsj-ffmpeg-toolkit

# Install core dependencies
pip install -e .

# Install optional dependencies (for advanced features)
pip install flask flask-socketio flask-cors psutil openai boto3 pandas plotly librosa pydub GPUtil

# Verify installation
python verify_installation.py
```

#### Linux/Mac/Termux
```bash
# Clone repository
git clone https://github.com/RAJSARASWATI-JATAV/rsj-ffmpeg-toolkit.git
cd rsj-ffmpeg-toolkit

# Run installer
chmod +x install.sh
./install.sh

# Verify installation
python3 verify_installation.py
```

### Method 2: Manual Installation

```bash
# 1. Clone repository
git clone https://github.com/RAJSARASWATI-JATAV/rsj-ffmpeg-toolkit.git
cd rsj-ffmpeg-toolkit

# 2. Install core dependencies
pip install click rich colorama fastapi uvicorn pydantic
pip install opencv-python Pillow numpy requests python-dotenv
pip install watchdog schedule PyYAML tqdm

# 3. Install package in development mode
pip install -e .

# 4. Install optional dependencies (choose what you need)

# For Dashboard & Analytics
pip install flask flask-socketio flask-cors psutil pandas plotly

# For AI Features (GPT Director)
pip install openai anthropic langchain

# For Cloud Processing
pip install boto3 google-cloud-storage azure-storage-blob

# For Audio Analysis
pip install librosa pydub

# For GPU Monitoring
pip install GPUtil

# 5. Verify installation
python verify_installation.py
```

---

## 📦 DEPENDENCY CATEGORIES

### Core Dependencies (Required)
These are automatically installed with `pip install -e .`:
- `click` - CLI framework
- `rich` - Terminal formatting
- `colorama` - Cross-platform colors
- `fastapi` - API server
- `uvicorn` - ASGI server
- `pydantic` - Data validation
- `opencv-python` - Video processing
- `Pillow` - Image processing
- `numpy` - Numerical operations
- `requests` - HTTP requests
- `python-dotenv` - Environment variables
- `watchdog` - File monitoring
- `schedule` - Task scheduling
- `PyYAML` - YAML parsing
- `tqdm` - Progress bars

### Optional Dependencies (For Advanced Features)

#### Dashboard & Analytics
```bash
pip install flask flask-socketio flask-cors psutil pandas plotly
```
**Enables:**
- Real-time web dashboard
- System monitoring
- Performance analytics
- Data visualization

#### AI Features
```bash
pip install openai anthropic langchain
```
**Enables:**
- GPT-powered video editing
- Natural language commands
- AI content analysis

#### Cloud Processing
```bash
pip install boto3 google-cloud-storage google-cloud-video-transcoder azure-storage-blob
```
**Enables:**
- AWS MediaConvert
- Google Cloud Transcoder
- Azure Media Services
- Cloudflare Stream

#### Audio Analysis
```bash
pip install librosa pydub
```
**Enables:**
- Beat detection
- Music analysis
- Advanced audio processing
- Montage creation

#### GPU Monitoring
```bash
pip install GPUtil
```
**Enables:**
- GPU usage monitoring
- Hardware acceleration stats

#### Bot Integration
```bash
pip install python-telegram-bot discord.py
```
**Enables:**
- Telegram bot
- Discord bot

---

## 🔧 POST-INSTALLATION SETUP

### 1. Configure API Keys (Optional)

Create a `.env` file in the project root:

```env
# OpenAI (for GPT Director)
OPENAI_API_KEY=your_openai_key_here

# Cloud Providers
AWS_ACCESS_KEY_ID=your_aws_key
AWS_SECRET_ACCESS_KEY=your_aws_secret
GCP_PROJECT_ID=your_gcp_project
AZURE_STORAGE_CONNECTION_STRING=your_azure_connection

# Bots
TELEGRAM_BOT_TOKEN=your_telegram_token
DISCORD_BOT_TOKEN=your_discord_token
```

### 2. Verify Installation

```bash
python verify_installation.py
```

Expected output:
```
✅ RSJToolkit
✅ GPTDirector
✅ CloudProcessor
✅ MontageEngine
✅ ContentAnalyzer
```

### 3. Test Basic Functionality

```bash
# Test CLI
python cli.py --version

# Test Python API
python -c "from rsj_ffmpeg import RSJToolkit; print(RSJToolkit().version)"
```

---

## 🎯 FEATURE-SPECIFIC INSTALLATION

### For Basic Video Processing Only
```bash
pip install -e .
# That's it! Core features work without optional deps
```

### For AI-Powered Editing
```bash
pip install -e .
pip install openai librosa
```

### For Cloud Processing
```bash
pip install -e .
pip install boto3 google-cloud-storage azure-storage-blob
```

### For Complete Installation (All Features)
```bash
pip install -e .
pip install flask flask-socketio flask-cors psutil pandas plotly
pip install openai anthropic langchain
pip install boto3 google-cloud-storage azure-storage-blob
pip install librosa pydub GPUtil
pip install python-telegram-bot discord.py
```

---

## 🐛 TROUBLESHOOTING

### Issue: "No module named 'rsj_ffmpeg'"
**Solution:**
```bash
pip install -e .
```

### Issue: "FFmpeg not found"
**Solution:**
- **Windows:** Download from [ffmpeg.org](https://ffmpeg.org) and add to PATH
- **Linux:** `sudo apt install ffmpeg`
- **Mac:** `brew install ffmpeg`
- **Termux:** `pkg install ffmpeg`

### Issue: "UnicodeDecodeError" during installation
**Solution:** Already fixed in setup.py with UTF-8 encoding

### Issue: Missing optional dependencies
**Solution:** Install only what you need:
```bash
# Check what's missing
python test_imports.py

# Install specific packages
pip install <package-name>
```

### Issue: Import errors
**Solution:**
```bash
# Reinstall package
pip uninstall rsj-ffmpeg
pip install -e .
```

---

## 📊 VERIFY YOUR INSTALLATION

Run the comprehensive test:
```bash
python test_imports.py
```

This will show:
- ✅ Working modules
- ❌ Missing dependencies
- Installation commands for missing packages

---

## 🎉 QUICK START AFTER INSTALLATION

### CLI Usage
```bash
# Convert video
python cli.py -i input.mp4 -o output.mp4

# Batch process
python cli.py --batch ./videos/ --export ./output/
```

### Python API
```python
from rsj_ffmpeg import RSJToolkit

toolkit = RSJToolkit()
toolkit.batch_convert(
    input_dir="./videos/",
    output_dir="./output/",
    enhance=True
)
```

### Start Dashboard (if Flask installed)
```bash
python dashboard/analytics_v2.py
# Open http://localhost:5001
```

### Start API Server
```bash
python api_server_v2.py
# API docs at http://localhost:8080/docs
```

---

## 📚 NEXT STEPS

1. ✅ Read [QUICKSTART.md](QUICKSTART.md)
2. ✅ Explore [examples/](examples/)
3. ✅ Check [RSJ-FFMPEG-TOOLKIT.md](RSJ-FFMPEG-TOOLKIT.md) for full documentation
4. ✅ Join community on Telegram

---

## 💡 TIPS

- Install only dependencies you need
- Use virtual environment for isolation
- Keep FFmpeg updated
- Check `config.json` for customization

---

**Built with 💀 by RAJSARASWATI JATAV**  
**© 2025 RAJSARASWATI JATAV | All Rights Reserved**