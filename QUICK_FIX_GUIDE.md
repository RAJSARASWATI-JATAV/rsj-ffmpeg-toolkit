# ⚡ RSJ-FFMPEG QUICK FIX GUIDE

**For immediate use without installing all dependencies**

---

## 🎯 CURRENT STATUS

✅ **Core Framework:** Fully functional  
✅ **All Modules:** Importable and working  
⚠️ **Optional Features:** Need additional packages

---

## 🚀 MINIMAL SETUP (5 Minutes)

### Step 1: Install Core Package
```bash
cd rsj-ffmpeg-toolkit
pip install -e .
```

### Step 2: Verify Core Works
```bash
python -c "from rsj_ffmpeg import RSJToolkit; print('✅ Core working!')"
```

### Step 3: Use Basic Features
```python
from rsj_ffmpeg import RSJToolkit

toolkit = RSJToolkit()

# Convert video
toolkit.batch_convert(
    input_dir="./videos/",
    output_dir="./output/",
    format="mp4"
)
```

**That's it! Core features work without any optional dependencies.**

---

## 📦 INSTALL FEATURES AS NEEDED

### Want Dashboard?
```bash
pip install flask flask-socketio flask-cors psutil pandas plotly
python dashboard/analytics_v2.py
```

### Want AI Editing?
```bash
pip install openai
# Set API key in .env or config.json
```

### Want Cloud Processing?
```bash
pip install boto3  # For AWS
# OR
pip install google-cloud-storage  # For GCP
# OR
pip install azure-storage-blob  # For Azure
```

### Want Audio Analysis?
```bash
pip install librosa pydub
```

---

## 🔧 WHAT WORKS WITHOUT OPTIONAL DEPS

### ✅ Core Video Processing
- Batch conversion
- Format conversion
- Video enhancement
- Watermarking
- Logo overlay
- Frame extraction
- Thumbnail generation
- GIF creation
- Video concatenation
- Video trimming

### ✅ Core Audio Processing
- Audio extraction
- Audio normalization
- Audio effects
- Channel extraction
- Audio/video merging

### ✅ Basic Automation
- Watch folder
- Task scheduling
- Batch processing

### ✅ CLI Interface
- All basic commands
- System check
- Help documentation

### ✅ API Server
- REST API endpoints
- File upload
- Job management

---

## ⚠️ WHAT NEEDS OPTIONAL DEPS

### Needs Flask/psutil
- Web dashboard
- Real-time monitoring
- Analytics visualization

### Needs OpenAI
- GPT Director
- Natural language editing

### Needs boto3/GCP/Azure SDKs
- Cloud processing
- Multi-cloud support

### Needs librosa
- Beat detection
- Music analysis
- Auto montage creation

### Needs GPUtil
- GPU monitoring
- Hardware stats

---

## 🎯 RECOMMENDED INSTALLATION ORDER

### For Most Users (Basic + Dashboard)
```bash
pip install -e .
pip install flask flask-socketio flask-cors psutil
```

### For AI Enthusiasts (+ AI Features)
```bash
pip install -e .
pip install flask flask-socketio flask-cors psutil
pip install openai librosa
```

### For Cloud Users (+ Cloud Processing)
```bash
pip install -e .
pip install flask flask-socketio flask-cors psutil
pip install boto3  # Choose your cloud provider
```

### For Power Users (Everything)
```bash
pip install -e .
pip install flask flask-socketio flask-cors psutil pandas plotly
pip install openai librosa pydub
pip install boto3 google-cloud-storage azure-storage-blob
pip install GPUtil python-telegram-bot discord.py
```

---

## 🐛 COMMON ISSUES & FIXES

### "No module named 'rsj_ffmpeg'"
```bash
pip install -e .
```

### "No module named 'flask'"
```bash
# Dashboard won't work, but core features will
# Install if you need dashboard:
pip install flask flask-socketio flask-cors
```

### "No module named 'openai'"
```bash
# GPT Director won't work, but everything else will
# Install if you need AI editing:
pip install openai
```

### "FFmpeg not found"
```bash
# Windows: Download from ffmpeg.org and add to PATH
# Linux: sudo apt install ffmpeg
# Mac: brew install ffmpeg
```

---

## ✅ VERIFICATION CHECKLIST

Run this to see what works:
```bash
python test_imports.py
```

Output shows:
- ✅ Working modules (green checkmarks)
- ❌ Missing optional dependencies (red X)
- Installation commands for missing packages

---

## 💡 PRO TIPS

1. **Start minimal, add features as needed**
2. **Core features work without any optional deps**
3. **Install only what you'll actually use**
4. **Use virtual environment to avoid conflicts**
5. **Check test_imports.py to see what's missing**

---

## 🎉 YOU'RE READY!

Even without optional dependencies, you can:
- ✅ Convert videos
- ✅ Process audio
- ✅ Batch operations
- ✅ Use CLI
- ✅ Use Python API
- ✅ Run automation

**Install optional features only when you need them!**

---

**Built with 💀 by RAJSARASWATI JATAV**