#!/usr/bin/env python3
"""
RSJ-FFMPEG Command Line Interface
Powerful CLI for multimedia processing
"""

import sys
import argparse
from pathlib import Path
from rsj_ffmpeg import RSJToolkit, BANNER
from rsj_ffmpeg.utils import system_check, generate_report


def print_banner():
    """Print RSJ-FFMPEG banner"""
    print(BANNER)


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description="RSJ-FFMPEG Power Toolkit - Ultimate Multimedia Automation",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Batch convert videos
  rsj-ffmpeg --batch ./videos/ --format mp4 --export ./output/
  
  # AI upscale with watermark
  rsj-ffmpeg -i video.mp4 --ai-upscale 4x --watermark "RAJSARASWATI JATAV" -o out.mp4
  
  # Create GIF
  rsj-ffmpeg -i video.mp4 --to-gif -o output.gif
  
  # Extract audio
  rsj-ffmpeg -i video.mp4 --extract-audio -o audio.mp3
  
  # Stream to YouTube
  rsj-ffmpeg --stream-yt YOUR_KEY --input webcam --overlay logo.png

© 2025 RAJSARASWATI JATAV | All Rights Reserved
        """
    )
    
    # Basic options
    parser.add_argument('-i', '--input', help='Input file or directory')
    parser.add_argument('-o', '--output', help='Output file')
    parser.add_argument('--version', action='version', version='RSJ-FFMPEG v2.2.0')
    parser.add_argument('--system-check', action='store_true', help='Check system dependencies')
    
    # Batch processing
    parser.add_argument('--batch', metavar='DIR', help='Batch process directory')
    parser.add_argument('--format', default='mp4', help='Output format (default: mp4)')
    parser.add_argument('--export', metavar='DIR', help='Export directory')
    
    # Video enhancement
    parser.add_argument('--ai-upscale', choices=['2x', '4x', '8x'], help='AI upscale factor')
    parser.add_argument('--enhance', action='store_true', help='Apply AI enhancement')
    parser.add_argument('--stabilize', action='store_true', help='Stabilize video')
    parser.add_argument('--denoise', action='store_true', help='Remove noise')
    
    # Watermark & branding
    parser.add_argument('--watermark', metavar='TEXT', help='Add text watermark')
    parser.add_argument('--logo', metavar='FILE', help='Add logo overlay')
    parser.add_argument('--branded-logo', metavar='FILE', help='Add branded logo')
    parser.add_argument('--watermark-position', 
                       choices=['top-left', 'top-right', 'bottom-left', 'bottom-right', 'center'],
                       default='bottom-right', help='Watermark position')
    
    # Video operations
    parser.add_argument('--to-gif', action='store_true', help='Convert to GIF')
    parser.add_argument('--extract-frames', action='store_true', help='Extract frames')
    parser.add_argument('--thumbnails', action='store_true', help='Generate thumbnails')
    parser.add_argument('--speed', type=float, help='Change speed (0.5 = half, 2.0 = double)')
    parser.add_argument('--trim', nargs=2, metavar=('START', 'END'), help='Trim video (HH:MM:SS)')
    
    # Audio operations
    parser.add_argument('--extract-audio', action='store_true', help='Extract audio')
    parser.add_argument('--normalize', action='store_true', help='Normalize audio')
    parser.add_argument('--fx', nargs='+', help='Audio effects (reverb, echo, compression, eq)')
    parser.add_argument('--waveform', action='store_true', help='Create waveform video')
    parser.add_argument('--spectrum', action='store_true', help='Create spectrum video')
    
    # Streaming
    parser.add_argument('--stream', metavar='URL', help='Stream to RTMP/SRT URL')
    parser.add_argument('--stream-yt', metavar='KEY', help='Stream to YouTube')
    parser.add_argument('--stream-fb', metavar='KEY', help='Stream to Facebook')
    parser.add_argument('--overlay', metavar='FILE', help='Overlay image for stream')
    parser.add_argument('--stats-overlay', action='store_true', help='Show stats overlay')
    
    # Metadata
    parser.add_argument('--metadata', nargs=2, action='append', metavar=('KEY', 'VALUE'), 
                       help='Set metadata (can be used multiple times)')
    parser.add_argument('--artist', help='Set artist metadata')
    
    # Reporting
    parser.add_argument('--report', choices=['json', 'markdown'], help='Generate report')
    parser.add_argument('--log', metavar='DIR', help='Log directory')
    
    # Advanced
    parser.add_argument('--plugin', action='append', help='Load custom plugin')
    parser.add_argument('--config', help='Configuration file path')
    
    args = parser.parse_args()
    
    # Print banner
    print_banner()
    
    # System check
    if args.system_check:
        print("\n[⚡] Running system check...\n")
        check = system_check()
        print(f"FFmpeg: {'✅ Installed' if check['ffmpeg'] else '❌ Not found'}")
        print(f"FFprobe: {'✅ Installed' if check['ffprobe'] else '❌ Not found'}")
        print(f"Python: {check['python_version']}")
        print(f"Platform: {check['platform']}")
        
        if not check['ffmpeg']:
            print("\n⚠️  FFmpeg is required. Install it from: https://ffmpeg.org/")
            sys.exit(1)
        
        print("\n✅ System check passed!\n")
        return
    
    # Initialize toolkit
    toolkit = RSJToolkit(config_path=args.config)
    
    # Batch processing
    if args.batch:
        print(f"\n[►] Batch processing: {args.batch}")
        print(f"[►] Output format: {args.format}")
        
        result = toolkit.batch_convert(
            input_dir=args.batch,
            output_dir=args.export or 'output',
            format=args.format,
            ai_upscale=args.ai_upscale,
            enhance=args.enhance,
            watermark=args.watermark,
            logo=args.logo or args.branded_logo
        )
        
        print(f"\n✅ Processed {result['summary']['total_jobs']} files")
        print(f"✅ Completed: {result['summary']['completed']}")
        print(f"❌ Failed: {result['summary']['failed']}")
        
        # Generate report
        if args.report:
            report_path = generate_report(result['jobs'], format=args.report)
            print(f"\n📊 Report generated: {report_path}")
        
        return
    
    # Single file processing
    if not args.input:
        parser.print_help()
        return
    
    output = args.output or f"output.{args.format}"
    
    # Convert to GIF
    if args.to_gif:
        print(f"\n[►] Creating GIF from {args.input}")
        result = toolkit.create_gif(args.input, output)
        print(f"✅ GIF created: {output}")
        return
    
    # Extract audio
    if args.extract_audio:
        print(f"\n[►] Extracting audio from {args.input}")
        result = toolkit.extract_audio(args.input, output)
        print(f"✅ Audio extracted: {output}")
        return
    
    # AI Enhancement
    if args.ai_upscale or args.enhance or args.stabilize:
        print(f"\n[►] AI Enhancement: {args.input}")
        if args.ai_upscale:
            print(f"[►] Upscaling: {args.ai_upscale}")
        if args.enhance:
            print(f"[►] Enhancing quality")
        if args.stabilize:
            print(f"[►] Stabilizing video")
        
        upscale_factor = int(args.ai_upscale.replace('x', '')) if args.ai_upscale else 1
        
        result = toolkit.ai_enhance(
            args.input,
            output,
            upscale=upscale_factor,
            denoise=args.denoise,
            stabilize=args.stabilize
        )
        print(f"✅ Enhancement complete: {output}")
        return
    
    # Add watermark
    if args.watermark:
        print(f"\n[►] Adding watermark: {args.watermark}")
        result = toolkit.add_watermark(
            args.input,
            output,
            args.watermark,
            position=args.watermark_position
        )
        print(f"✅ Watermark added: {output}")
        return
    
    # Streaming
    if args.stream or args.stream_yt or args.stream_fb:
        platform = "custom"
        key = args.stream
        
        if args.stream_yt:
            platform = "youtube"
            key = args.stream_yt
        elif args.stream_fb:
            platform = "facebook"
            key = args.stream_fb
        
        print(f"\n[►] Starting stream to {platform}")
        stream_info = toolkit.start_stream(
            platform=platform,
            key=key,
            input_source=args.input or "webcam",
            overlay=args.overlay,
            stats=args.stats_overlay
        )
        
        print(f"\n🔴 LIVE STREAMING")
        print(f"Platform: {platform}")
        print(f"Command: {stream_info['command']}")
        print(f"\nPress Ctrl+C to stop streaming")
        return
    
    # Default: show help
    parser.print_help()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Operation cancelled by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)