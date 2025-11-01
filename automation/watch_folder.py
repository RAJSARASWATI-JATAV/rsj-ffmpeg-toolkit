#!/usr/bin/env python3
"""
RSJ-FFMPEG Watch Folder Automation
Automatically process videos when added to a folder
"""

try:
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler
except ImportError:
    print("⚠️  watchdog not installed. Install with: pip install watchdog")
    exit(1)

import time
import argparse
from pathlib import Path
from rsj_ffmpeg import RSJToolkit, BANNER


class VideoHandler(FileSystemEventHandler):
    """Handle video file events"""
    
    def __init__(self, toolkit: RSJToolkit, output_dir: str, **kwargs):
        self.toolkit = toolkit
        self.output_dir = output_dir
        self.options = kwargs
        self.processing = set()
        
        Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    def on_created(self, event):
        """Handle file creation"""
        if event.is_directory:
            return
        
        file_path = event.src_path
        
        # Check if video file
        video_extensions = ['.mp4', '.avi', '.mkv', '.mov', '.flv', '.wmv']
        if not any(file_path.endswith(ext) for ext in video_extensions):
            return
        
        # Avoid processing same file multiple times
        if file_path in self.processing:
            return
        
        self.processing.add(file_path)
        
        print(f"\n[►] New video detected: {Path(file_path).name}")
        
        # Wait for file to be completely written
        time.sleep(2)
        
        # Process video
        self.process_video(file_path)
        
        self.processing.remove(file_path)
    
    def process_video(self, input_file: str):
        """Process video with configured options"""
        output_file = Path(self.output_dir) / Path(input_file).name
        
        print(f"[►] Processing: {Path(input_file).name}")
        
        try:
            # Apply enhancements
            if self.options.get('ai_upscale'):
                print(f"[►] AI Upscaling: {self.options['ai_upscale']}")
            
            if self.options.get('enhance'):
                print(f"[►] Enhancing quality")
            
            if self.options.get('watermark'):
                print(f"[►] Adding watermark: {self.options['watermark']}")
            
            # Process
            result = self.toolkit.batch_convert(
                input_dir=str(Path(input_file).parent),
                output_dir=self.output_dir,
                **self.options
            )
            
            print(f"✅ Processed: {output_file.name}")
            
        except Exception as e:
            print(f"❌ Error processing {Path(input_file).name}: {e}")


def main():
    """Main watch folder automation"""
    parser = argparse.ArgumentParser(
        description="RSJ-FFMPEG Watch Folder Automation"
    )
    
    parser.add_argument('--watch', required=True, help='Directory to watch')
    parser.add_argument('--output', required=True, help='Output directory')
    parser.add_argument('--ai-upscale', choices=['2x', '4x', '8x'], help='AI upscale')
    parser.add_argument('--enhance', action='store_true', help='Enhance quality')
    parser.add_argument('--watermark', help='Watermark text')
    parser.add_argument('--format', default='mp4', help='Output format')
    
    args = parser.parse_args()
    
    print(BANNER)
    print("\n🔍 RSJ-FFMPEG Watch Folder Automation")
    print(f"📁 Watching: {args.watch}")
    print(f"📤 Output: {args.output}")
    
    if args.ai_upscale:
        print(f"🎨 AI Upscale: {args.ai_upscale}")
    if args.enhance:
        print(f"✨ Enhancement: Enabled")
    if args.watermark:
        print(f"🏷️  Watermark: {args.watermark}")
    
    print("\n⏳ Waiting for new videos...")
    print("Press Ctrl+C to stop\n")
    
    # Initialize toolkit
    toolkit = RSJToolkit()
    
    # Create event handler
    event_handler = VideoHandler(
        toolkit=toolkit,
        output_dir=args.output,
        ai_upscale=args.ai_upscale,
        enhance=args.enhance,
        watermark=args.watermark,
        format=args.format
    )
    
    # Create observer
    observer = Observer()
    observer.schedule(event_handler, args.watch, recursive=False)
    observer.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n\n⚠️  Stopping watch folder automation...")
        observer.stop()
    
    observer.join()
    print("✅ Stopped\n")
    print("© 2025 RAJSARASWATI JATAV | All Rights Reserved")


if __name__ == "__main__":
    main()