#!/bin/bash
# RSJ-FFMPEG Batch Automation Script
# Automate video processing workflows
# © 2025 RAJSARASWATI JATAV

echo "🔥 RSJ-FFMPEG Batch Automation 🔥"
echo "=================================="
echo ""

# Configuration
INPUT_DIR="./input/videos"
OUTPUT_DIR="./output/processed"
WATERMARK="© RAJSARASWATI JATAV 2025"

# Create output directory
mkdir -p "$OUTPUT_DIR"

# Example 1: Batch convert all videos to MP4
echo "[1] Batch converting to MP4..."
rsj-ffmpeg --batch "$INPUT_DIR" --format mp4 --export "$OUTPUT_DIR/mp4/"

# Example 2: Batch upscale with AI
echo "[2] AI upscaling videos..."
rsj-ffmpeg --batch "$INPUT_DIR" \
  --ai-upscale 2x \
  --enhance \
  --export "$OUTPUT_DIR/upscaled/"

# Example 3: Add watermark to all videos
echo "[3] Adding watermarks..."
for video in "$INPUT_DIR"/*.mp4; do
  filename=$(basename "$video")
  rsj-ffmpeg -i "$video" \
    --watermark "$WATERMARK" \
    --watermark-position bottom-right \
    -o "$OUTPUT_DIR/watermarked/$filename"
done

# Example 4: Create thumbnails for all videos
echo "[4] Generating thumbnails..."
rsj-ffmpeg --batch "$INPUT_DIR" \
  --thumbnails \
  --export "$OUTPUT_DIR/thumbnails/"

# Example 5: Extract audio from all videos
echo "[5] Extracting audio..."
for video in "$INPUT_DIR"/*.mp4; do
  filename=$(basename "$video" .mp4)
  rsj-ffmpeg -i "$video" \
    --extract-audio \
    -o "$OUTPUT_DIR/audio/${filename}.mp3"
done

# Example 6: Create GIFs from videos
echo "[6] Creating GIFs..."
for video in "$INPUT_DIR"/*.mp4; do
  filename=$(basename "$video" .mp4)
  rsj-ffmpeg -i "$video" \
    --to-gif \
    -o "$OUTPUT_DIR/gifs/${filename}.gif"
done

# Generate report
echo "[7] Generating report..."
rsj-ffmpeg --batch "$INPUT_DIR" \
  --report markdown \
  --export "$OUTPUT_DIR/"

echo ""
echo "✅ Batch automation completed!"
echo "📊 Check $OUTPUT_DIR for results"
echo ""
echo "© 2025 RAJSARASWATI JATAV | All Rights Reserved"