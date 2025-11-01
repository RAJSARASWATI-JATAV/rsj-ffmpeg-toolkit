#!/usr/bin/env python3
"""
RSJ-FFMPEG Advanced Usage Examples
Advanced features and workflows
"""

from rsj_ffmpeg import RSJToolkit
from rsj_ffmpeg.video import VideoProcessor
from rsj_ffmpeg.audio import AudioProcessor
from rsj_ffmpeg.utils import generate_report

# Initialize
toolkit = RSJToolkit(config_path="config.json")
video_processor = VideoProcessor(toolkit.config)
audio_processor = AudioProcessor(toolkit.config)

print("🔥 RSJ-FFMPEG Advanced Examples 🔥\n")

# Example 1: Extract Frames for AI Training
print("Example 1: Extract Frames")
result = video_processor.extract_frames(
    input_file="./input/video.mp4",
    output_dir="./output/frames/",
    fps=1,
    format="png"
)
print(f"Frames extracted: {result['status']}\n")

# Example 2: Create Thumbnails
print("Example 2: Create Thumbnails")
for i, timestamp in enumerate(["00:00:05", "00:00:15", "00:00:30"]):
    result = video_processor.create_thumbnail(
        input_file="./input/video.mp4",
        output_file=f"./output/thumb_{i+1}.jpg",
        timestamp=timestamp,
        width=1280
    )
    print(f"Thumbnail {i+1}: {result['status']}")
print()

# Example 3: Change Video Speed
print("Example 3: Slow Motion (0.5x)")
result = video_processor.change_speed(
    input_file="./input/action.mp4",
    output_file="./output/slow_motion.mp4",
    speed=0.5
)
print(f"Slow motion: {result['status']}\n")

# Example 4: Concatenate Videos
print("Example 4: Concatenate Videos")
result = video_processor.concatenate_videos(
    input_files=[
        "./input/intro.mp4",
        "./input/main.mp4",
        "./input/outro.mp4"
    ],
    output_file="./output/complete.mp4"
)
print(f"Concatenation: {result['status']}\n")

# Example 5: Audio Normalization
print("Example 5: Normalize Audio")
result = audio_processor.normalize_audio(
    input_file="./input/audio.mp3",
    output_file="./output/normalized.mp3",
    target_level=-23.0
)
print(f"Normalization: {result['status']}\n")

# Example 6: Apply Audio Effects
print("Example 6: Audio Effects")
result = audio_processor.apply_audio_effects(
    input_file="./input/audio.mp3",
    output_file="./output/effects.mp3",
    effects=["reverb", "compression", "bass_boost"]
)
print(f"Effects applied: {result['status']}\n")

# Example 7: Create Waveform Video
print("Example 7: Waveform Visualization")
result = audio_processor.create_waveform_video(
    audio_file="./input/music.mp3",
    output_file="./output/waveform.mp4",
    width=1920,
    height=1080
)
print(f"Waveform video: {result['status']}\n")

# Example 8: Create Spectrum Video
print("Example 8: Spectrum Analyzer")
result = audio_processor.create_spectrum_video(
    audio_file="./input/music.mp3",
    output_file="./output/spectrum.mp4",
    width=1920,
    height=1080
)
print(f"Spectrum video: {result['status']}\n")

# Example 9: Stabilize Video
print("Example 9: Video Stabilization")
result = video_processor.stabilize_video(
    input_file="./input/shaky.mp4",
    output_file="./output/stabilized.mp4"
)
print(f"Stabilization: {result['status']}\n")

# Example 10: Trim Video
print("Example 10: Trim Video")
result = video_processor.trim_video(
    input_file="./input/long_video.mp4",
    output_file="./output/trimmed.mp4",
    start_time="00:01:00",
    end_time="00:02:30"
)
print(f"Trimming: {result['status']}\n")

print("✅ All advanced examples completed!")
print("© 2025 RAJSARASWATI JATAV | All Rights Reserved")