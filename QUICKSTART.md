# 🚀 RSJ-FFMPEG QUICK START GUIDE

Get started with the RSJ-FFMPEG Power Toolkit in minutes!

## ⚡ Installation

### Linux / Mac / Termux
```bash
# Clone repository
git clone https://github.com/RAJSARASWATI-JATAV/rsj-ffmpeg-toolkit.git
cd rsj-ffmpeg-toolkit

# Run installer
chmod +x install.sh
./install.sh
```

### Windows
```powershell
# Clone repository
git clone https://github.com/RAJSARASWATI-JATAV/rsj-ffmpeg-toolkit.git
cd rsj-ffmpeg-toolkit

# Run installer
.\install.ps1
```

## ✅ Verify Installation

```bash
# Check if installed
rsj-ffmpeg --version

# System check
rsj-ffmpeg --system-check
```

## 🎯 Basic Usage

### 1. Convert Video Format
```bash
rsj-ffmpeg -i input.avi -o output.mp4
```

### 2. Batch Convert Directory
```bash
rsj-ffmpeg --batch ./videos/ --format mp4 --export ./output/
```

### 3. AI Upscale Video
```bash
rsj-ffmpeg -i video.mp4 --ai-upscale 4x -o upscaled.mp4
```

### 4. Add Watermark
```bash
rsj-ffmpeg -i video.mp4 --watermark "RAJSARASWATI JATAV" -o branded.mp4
```

### 5. Create GIF
```bash
rsj-ffmpeg -i video.mp4 --to-gif -o animation.gif
```

### 6. Extract Audio
```bash
rsj-ffmpeg -i video.mp4 --extract-audio -o audio.mp3
```

### 7. Enhance Video Quality
```bash
rsj-ffmpeg -i video.mp4 --enhance --stabilize --denoise -o enhanced.mp4
```

### 8. Create Waveform Video
```bash
rsj-ffmpeg -i music.mp3 --waveform -o visualizer.mp4
```

## 🔥 Advanced Examples

### Batch Processing with AI Enhancement
```bash
rsj-ffmpeg --batch ./raw_videos/ \
  --ai-upscale 2x \
  --enhance \
  --watermark "© RAJSARASWATI JATAV 2025" \
  --export ./processed/ \
  --report json
```

### Complete Video Production Pipeline
```bash
# 1. Upscale
rsj-ffmpeg -i raw.mp4 --ai-upscale 4x -o upscaled.mp4

# 2. Enhance
rsj-ffmpeg -i upscaled.mp4 --enhance --stabilize -o enhanced.mp4

# 3. Add branding
rsj-ffmpeg -i enhanced.mp4 \
  --watermark "RAJSARASWATI JATAV" \
  --logo rsj-logo.png \
  -o final.mp4
```

### Audio Processing
```bash
# Normalize audio
rsj-ffmpeg -i audio.mp3 --normalize -o normalized.mp3

# Apply effects
rsj-ffmpeg -i audio.mp3 --fx reverb echo compression -o effects.mp3
```

## 📚 Python API Usage

```python
from rsj_ffmpeg import RSJToolkit

# Initialize
toolkit = RSJToolkit()

# Batch convert
result = toolkit.batch_convert(
    input_dir="./videos/",
    output_dir="./output/",
    ai_upscale="4x",
    enhance=True,
    watermark="RAJSARASWATI JATAV"
)

# AI enhancement
toolkit.ai_enhance(
    input_file="video.mp4",
    output_file="enhanced.mp4",
    upscale=4,
    denoise=True,
    stabilize=True
)

# Create GIF
toolkit.create_gif(
    input_file="video.mp4",
    output_file="animation.gif",
    duration=5,
    fps=15
)
```

## 🎓 Learn More

- Full Documentation: [RSJ-FFMPEG-TOOLKIT.md](RSJ-FFMPEG-TOOLKIT.md)
- Examples: Check the `examples/` directory
- Help: `rsj-ffmpeg --help`

## 🆘 Troubleshooting

### FFmpeg not found
```bash
# Linux/Termux
sudo apt-get install ffmpeg
# or
pkg install ffmpeg

# Mac
brew install ffmpeg

# Windows
winget install FFmpeg
```

### Permission denied
```bash
chmod +x install.sh
chmod +x cli.py
```

### Python module not found
```bash
pip3 install -r requirements.txt
pip3 install -e .
```

## 🌟 Next Steps

1. Check out [examples/](examples/) for more use cases
2. Read the full [documentation](RSJ-FFMPEG-TOOLKIT.md)
3. Join the community on [Telegram](https://t.me/rajsaraswatijatav)
4. Star the repo on [GitHub](https://github.com/RAJSARASWATI-JATAV)

---

**🟢 STAY POWERFUL. STAY CREATIVE. UPGRADE YOURSELF! 🟢**

**© 2025 RAJSARASWATI JATAV | All Rights Reserved**