# 🧪 RSJ-FFMPEG Testing Guide

Quick testing guide to verify your installation and functionality.

## ✅ Installation Test

```bash
# 1. Check Python
python3 --version

# 2. Check FFmpeg
ffmpeg -version

# 3. Check RSJ-FFMPEG
rsj-ffmpeg --version

# 4. System check
rsj-ffmpeg --system-check
```

Expected output:
```
✅ FFmpeg: Installed
✅ FFprobe: Installed
✅ Python: 3.x.x
✅ Platform: Linux/Windows/Darwin
```

## 🎬 Basic Functionality Tests

### Test 1: Help Command
```bash
rsj-ffmpeg --help
```
Should display full help menu with all options.

### Test 2: Video Info
```bash
# Create a test video first (if you don't have one)
ffmpeg -f lavfi -i testsrc=duration=10:size=1280x720:rate=30 test_input.mp4

# Get info
rsj-ffmpeg -i test_input.mp4
```

### Test 3: Simple Conversion
```bash
rsj-ffmpeg -i test_input.mp4 -o test_output.mp4
```

### Test 4: Add Watermark
```bash
rsj-ffmpeg -i test_input.mp4 --watermark "TEST" -o test_watermark.mp4
```

### Test 5: Create GIF
```bash
rsj-ffmpeg -i test_input.mp4 --to-gif -o test.gif
```

## 🐍 Python API Test

Create `test_api.py`:
```python
from rsj_ffmpeg import RSJToolkit

# Initialize
toolkit = RSJToolkit()
print("✅ Toolkit initialized")

# Test video info
info = toolkit.get_video_info("test_input.mp4")
print(f"✅ Video info retrieved: {info.get('format', {}).get('duration', 'N/A')}s")

print("\n✅ All API tests passed!")
```

Run:
```bash
python3 test_api.py
```

## 📊 Batch Processing Test

```bash
# Create test directory
mkdir -p test_batch/input test_batch/output

# Copy test video
cp test_input.mp4 test_batch/input/

# Batch process
rsj-ffmpeg --batch test_batch/input/ --export test_batch/output/

# Check output
ls -la test_batch/output/
```

## 🧹 Cleanup

```bash
# Remove test files
rm -f test_input.mp4 test_output.mp4 test_watermark.mp4 test.gif
rm -rf test_batch/
```

## 🐛 Troubleshooting

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

### Module not found
```bash
pip3 install -r requirements.txt
pip3 install -e .
```

## ✅ Success Criteria

All tests should:
- ✅ Execute without errors
- ✅ Produce expected output files
- ✅ Display success messages
- ✅ Complete in reasonable time

---

**© 2025 RAJSARASWATI JATAV | All Rights Reserved**