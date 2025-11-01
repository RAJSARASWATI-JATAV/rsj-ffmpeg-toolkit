# 📚 RSJ-FFMPEG Examples

This directory contains example scripts demonstrating various features of the RSJ-FFMPEG Power Toolkit.

## 📁 Files

### 1. `basic_usage.py`
Basic examples covering common use cases:
- Batch video conversion
- AI enhancement
- GIF creation
- Audio extraction
- Watermarking
- Video information retrieval

**Run:**
```bash
python3 examples/basic_usage.py
```

### 2. `advanced_usage.py`
Advanced features and workflows:
- Frame extraction for AI training
- Thumbnail generation
- Video speed manipulation
- Video concatenation
- Audio normalization
- Audio effects
- Waveform/spectrum visualization
- Video stabilization
- Video trimming

**Run:**
```bash
python3 examples/advanced_usage.py
```

### 3. `batch_automation.sh`
Bash script for automated batch processing:
- Batch format conversion
- AI upscaling
- Watermark addition
- Thumbnail generation
- Audio extraction
- GIF creation
- Report generation

**Run:**
```bash
chmod +x examples/batch_automation.sh
./examples/batch_automation.sh
```

## 🎯 Quick Examples

### Convert Single Video
```bash
rsj-ffmpeg -i input.mp4 -o output.mp4
```

### Batch Process Directory
```bash
rsj-ffmpeg --batch ./videos/ --format mp4 --export ./output/
```

### AI Upscale
```bash
rsj-ffmpeg -i video.mp4 --ai-upscale 4x -o upscaled.mp4
```

### Add Watermark
```bash
rsj-ffmpeg -i video.mp4 --watermark "RAJSARASWATI JATAV" -o branded.mp4
```

### Create GIF
```bash
rsj-ffmpeg -i video.mp4 --to-gif -o animation.gif
```

### Extract Audio
```bash
rsj-ffmpeg -i video.mp4 --extract-audio -o audio.mp3
```

## 📖 Learn More

- [Full Documentation](../RSJ-FFMPEG-TOOLKIT.md)
- [Quick Start Guide](../QUICKSTART.md)
- [Main README](../README.md)

---

**© 2025 RAJSARASWATI JATAV | All Rights Reserved**