#!/usr/bin/env python3
"""
RSJ-FFMPEG Montage Engine Examples
Automatic video montage creation demonstrations

Author: RAJSARASWATI JATAV
Version: 2.2.0
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from rsj_ffmpeg.montage_engine import MontageEngine


def example_1_cinematic_montage():
    """Example 1: Create cinematic montage"""
    print("=" * 60)
    print("Example 1: Cinematic Montage")
    print("=" * 60)
    
    engine = MontageEngine(config={})
    
    result = engine.create_auto_montage(
        input_dir="./clips/",
        output="cinematic_montage.mp4",
        style="cinematic",
        duration=120,  # 2 minutes
        music="cinematic_music.mp3",
        watermark="© RAJSARASWATI JATAV 2025"
    )
    
    print(f"\n✅ Result: {result['status']}")
    if result['status'] == 'success':
        print(f"📁 Output: {result['output']}")
        print(f"🎬 Clips used: {result['clips_used']}")


def example_2_sports_highlight():
    """Example 2: Sports highlight reel"""
    print("\n" + "=" * 60)
    print("Example 2: Sports Highlight Reel")
    print("=" * 60)
    
    engine = MontageEngine(config={})
    
    result = engine.create_auto_montage(
        input_dir="./sports_clips/",
        output="sports_highlights.mp4",
        style="sports",
        duration=90,
        music="energetic_music.mp3"
    )
    
    print(f"\n✅ Result: {result['status']}")


def example_3_travel_montage():
    """Example 3: Travel montage"""
    print("\n" + "=" * 60)
    print("Example 3: Travel Montage")
    print("=" * 60)
    
    engine = MontageEngine(config={})
    
    result = engine.create_auto_montage(
        input_dir="./travel_footage/",
        output="travel_montage.mp4",
        style="travel",
        duration=180,  # 3 minutes
        music="travel_music.mp3",
        title="My Amazing Journey"
    )
    
    print(f"\n✅ Result: {result['status']}")


def example_4_beat_synced():
    """Example 4: Beat-synchronized music video"""
    print("\n" + "=" * 60)
    print("Example 4: Beat-Synchronized Montage")
    print("=" * 60)
    
    engine = MontageEngine(config={})
    
    result = engine.create_beat_synced_montage(
        input_dir="./music_video_clips/",
        music="song.mp3",
        output="music_video.mp4",
        style="music_video"
    )
    
    print(f"\n✅ Result: {result['status']}")


def example_5_wedding_montage():
    """Example 5: Wedding montage"""
    print("\n" + "=" * 60)
    print("Example 5: Wedding Montage")
    print("=" * 60)
    
    engine = MontageEngine(config={})
    
    result = engine.create_auto_montage(
        input_dir="./wedding_footage/",
        output="wedding_montage.mp4",
        style="wedding",
        duration=240,  # 4 minutes
        music="romantic_music.mp3",
        title="Sarah & John - June 15, 2025"
    )
    
    print(f"\n✅ Result: {result['status']}")


def example_6_action_montage():
    """Example 6: Fast-paced action montage"""
    print("\n" + "=" * 60)
    print("Example 6: Action Montage")
    print("=" * 60)
    
    engine = MontageEngine(config={})
    
    result = engine.create_auto_montage(
        input_dir="./action_clips/",
        output="action_montage.mp4",
        style="action",
        duration=60,  # 1 minute
        music="intense_music.mp3"
    )
    
    print(f"\n✅ Result: {result['status']}")


def example_7_vlog_montage():
    """Example 7: Vlog-style montage"""
    print("\n" + "=" * 60)
    print("Example 7: Vlog Montage")
    print("=" * 60)
    
    engine = MontageEngine(config={})
    
    result = engine.create_auto_montage(
        input_dir="./vlog_clips/",
        output="vlog_montage.mp4",
        style="vlog",
        duration=150,
        music="background_music.mp3",
        title="My Week in Review"
    )
    
    print(f"\n✅ Result: {result['status']}")


def main():
    """Run all examples"""
    print("\n🎬 RSJ-FFMPEG Montage Engine Examples")
    print("Author: RAJSARASWATI JATAV")
    print("Version: 2.2.0\n")
    
    print("⚠️  Note: Make sure you have:")
    print("  1. Video clips in the specified directories")
    print("  2. Music files for background audio")
    print("  3. FFmpeg installed and in PATH\n")
    
    try:
        # Run examples
        # Uncomment the examples you want to run
        
        # example_1_cinematic_montage()
        # example_2_sports_highlight()
        # example_3_travel_montage()
        # example_4_beat_synced()
        # example_5_wedding_montage()
        # example_6_action_montage()
        # example_7_vlog_montage()
        
        print("\n✅ Examples completed!")
        print("\n💡 Available Styles:")
        print("  - cinematic: Slow, dramatic editing")
        print("  - sports: Fast-paced, energetic")
        print("  - travel: Medium pace, scenic")
        print("  - wedding: Romantic, elegant")
        print("  - vlog: Casual, personal")
        print("  - action: Very fast, intense")
        print("  - music_video: Beat-synchronized")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")


if __name__ == "__main__":
    main()