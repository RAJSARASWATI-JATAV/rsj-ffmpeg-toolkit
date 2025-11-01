#!/usr/bin/env python3
"""
RSJ-FFMPEG Basic Usage Examples
Learn how to use the toolkit programmatically
"""

from rsj_ffmpeg import RSJToolkit

# Initialize toolkit
toolkit = RSJToolkit()

# Example 1: Batch convert videos
print("Example 1: Batch Convert")
result = toolkit.batch_convert(
    input_dir="./input/videos/",
    output_dir="./output/converted/",
    format="mp4",
    ai_upscale="2x",
    enhance=True,
    watermark="RAJSARASWATI JATAV"
)
print(f"Processed {result['summary']['total_jobs']} videos")

# Example 2: AI Enhancement
print("\nExample 2: AI Enhancement")
result = toolkit.ai_enhance(
    input_file="./input/video.mp4",
    output_file="./output/enhanced.mp4",
    upscale=4,
    denoise=True,
    stabilize=True
)
print(f"Enhancement status: {result['status']}")

# Example 3: Create GIF
print("\nExample 3: Create GIF")
result = toolkit.create_gif(
    input_file="./input/video.mp4",
    output_file="./output/animation.gif",
    start_time="00:00:10",
    duration=5,
    fps=15,
    width=640
)
print(f"GIF created: {result['status']}")

# Example 4: Extract Audio
print("\nExample 4: Extract Audio")
result = toolkit.extract_audio(
    input_file="./input/video.mp4",
    output_file="./output/audio.mp3"
)
print(f"Audio extracted: {result['status']}")

# Example 5: Add Watermark
print("\nExample 5: Add Watermark")
result = toolkit.add_watermark(
    input_file="./input/video.mp4",
    output_file="./output/watermarked.mp4",
    watermark_text="© RAJSARASWATI JATAV 2025",
    position="bottom-right",
    opacity=0.7
)
print(f"Watermark added: {result['status']}")

# Example 6: Get Video Info
print("\nExample 6: Get Video Info")
info = toolkit.get_video_info("./input/video.mp4")
if "format" in info:
    print(f"Duration: {info['format'].get('duration', 'N/A')}s")
    print(f"Size: {info['format'].get('size', 'N/A')} bytes")

print("\n✅ All examples completed!")
print("© 2025 RAJSARASWATI JATAV | All Rights Reserved")