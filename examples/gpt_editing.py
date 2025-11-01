#!/usr/bin/env python3
"""
RSJ-FFMPEG GPT Director Examples
Natural language video editing demonstrations

Author: RAJSARASWATI JATAV
Version: 2.2.0
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from rsj_ffmpeg.gpt_director import GPTDirector


def example_1_simple_prompt():
    """Example 1: Simple natural language editing"""
    print("=" * 60)
    print("Example 1: Simple Natural Language Editing")
    print("=" * 60)
    
    director = GPTDirector(
        config={},
        api_key=os.getenv("OPENAI_API_KEY")  # Set your API key
    )
    
    # Edit with natural language
    result = director.edit_from_prompt(
        input_files=["clip1.mp4", "clip2.mp4", "clip3.mp4"],
        prompt="Create a 2-minute energetic highlight reel with fast cuts and upbeat music",
        output="highlight_reel.mp4",
        duration=120
    )
    
    print(f"\n✅ Result: {result['status']}")
    if result['status'] == 'success':
        print(f"📁 Output: {result['output']}")


def example_2_cinematic_edit():
    """Example 2: Cinematic style editing"""
    print("\n" + "=" * 60)
    print("Example 2: Cinematic Style Editing")
    print("=" * 60)
    
    director = GPTDirector(config={})
    
    result = director.edit_from_prompt(
        input_files=["scene1.mp4", "scene2.mp4", "scene3.mp4"],
        prompt="Create a cinematic video with slow motion, dramatic transitions, and color grading",
        output="cinematic.mp4",
        style="cinematic",
        music="background_music.mp3"
    )
    
    print(f"\n✅ Result: {result['status']}")


def example_3_script_based():
    """Example 3: Script-based editing"""
    print("\n" + "=" * 60)
    print("Example 3: Script-Based Editing")
    print("=" * 60)
    
    # Create sample script
    script = """
SCENE 1: INT. OFFICE - DAY
John enters the office and sits at his desk.

JOHN
(looking at computer)
This project is going to be amazing!

SCENE 2: EXT. PARK - AFTERNOON
Sarah walks through the park, enjoying the sunshine.

SARAH
What a beautiful day!

SCENE 3: INT. COFFEE SHOP - EVENING
John and Sarah meet for coffee.

JOHN
I'm glad we could meet up.

SARAH
Me too! Let's discuss the project.
"""
    
    director = GPTDirector(config={})
    
    result = director.edit_from_script(
        script=script,
        footage_dir="./footage/",
        output="scripted_video.mp4",
        auto_select=True
    )
    
    print(f"\n✅ Result: {result['status']}")


def example_4_content_analysis():
    """Example 4: Video content analysis"""
    print("\n" + "=" * 60)
    print("Example 4: Video Content Analysis")
    print("=" * 60)
    
    director = GPTDirector(config={})
    
    # Analyze video content
    analysis = director.analyze_content(
        video_file="sample_video.mp4",
        analyze_audio=True,
        detect_scenes=True
    )
    
    print(f"\n📊 Analysis Results:")
    print(f"  Duration: {analysis.get('duration', 0):.2f} seconds")
    print(f"  Scenes detected: {len(analysis.get('scenes', []))}")
    print(f"  Has audio: {analysis.get('audio_analysis', {}).get('has_audio', False)}")
    
    # Show scenes
    if analysis.get('scenes'):
        print(f"\n🎬 Scene Changes:")
        for i, scene in enumerate(analysis['scenes'][:5], 1):
            print(f"  {i}. {scene['timestamp']:.2f}s - {scene['type']}")


def example_5_advanced_prompt():
    """Example 5: Advanced multi-style editing"""
    print("\n" + "=" * 60)
    print("Example 5: Advanced Multi-Style Editing")
    print("=" * 60)
    
    director = GPTDirector(config={})
    
    # Complex editing request
    result = director.edit_from_prompt(
        input_files=[
            "intro.mp4",
            "main_content_1.mp4",
            "main_content_2.mp4",
            "main_content_3.mp4",
            "outro.mp4"
        ],
        prompt="""
        Create a professional video with:
        - Fade in from black at the start
        - Cinematic color grading throughout
        - Smooth transitions between clips
        - Add slow motion to highlight important moments
        - Sync cuts to music beats
        - Add text overlays for key points
        - Fade out to black at the end
        """,
        output="professional_edit.mp4",
        music="soundtrack.mp3"
    )
    
    print(f"\n✅ Result: {result['status']}")


def example_6_batch_editing():
    """Example 6: Batch editing with GPT"""
    print("\n" + "=" * 60)
    print("Example 6: Batch Editing Multiple Videos")
    print("=" * 60)
    
    director = GPTDirector(config={})
    
    # Edit multiple videos with same style
    videos = [
        ("vlog_day1.mp4", "Day 1 vlog"),
        ("vlog_day2.mp4", "Day 2 vlog"),
        ("vlog_day3.mp4", "Day 3 vlog")
    ]
    
    for video_file, title in videos:
        print(f"\n📹 Processing: {title}")
        
        result = director.edit_from_prompt(
            input_files=[video_file],
            prompt=f"Create a casual vlog-style edit with jump cuts and text overlays. Add title: {title}",
            output=f"edited_{video_file}",
            style="vlog"
        )
        
        print(f"  ✅ Status: {result['status']}")


def main():
    """Run all examples"""
    print("\n🎬 RSJ-FFMPEG GPT Director Examples")
    print("Author: RAJSARASWATI JATAV")
    print("Version: 2.2.0\n")
    
    # Note: These examples assume you have video files
    # Replace with your actual file paths
    
    print("⚠️  Note: Make sure you have:")
    print("  1. Set OPENAI_API_KEY environment variable")
    print("  2. Video files in the correct locations")
    print("  3. FFmpeg installed and in PATH\n")
    
    try:
        # Run examples
        # Uncomment the examples you want to run
        
        # example_1_simple_prompt()
        # example_2_cinematic_edit()
        # example_3_script_based()
        # example_4_content_analysis()
        # example_5_advanced_prompt()
        # example_6_batch_editing()
        
        print("\n✅ Examples completed!")
        print("\n💡 Tip: Edit this file to uncomment and run specific examples")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nMake sure you have:")
        print("  - Valid API key set")
        print("  - Video files available")
        print("  - All dependencies installed")


if __name__ == "__main__":
    main()