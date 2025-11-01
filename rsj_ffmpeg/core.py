"""
RSJ-FFMPEG Core Toolkit
Main class for all multimedia operations
"""

import os
import json
import subprocess
from pathlib import Path
from typing import Optional, Dict, List, Any
from datetime import datetime


class RSJToolkit:
    """
    Main RSJ-FFMPEG Toolkit Class
    Provides all multimedia processing capabilities
    """
    
    def __init__(self, config_path: Optional[str] = None, api_key: Optional[str] = None):
        """Initialize RSJ Toolkit"""
        self.version = "2.2.0"
        self.author = "RAJSARASWATI JATAV"
        self.api_key = api_key
        
        # Load configuration
        if config_path and os.path.exists(config_path):
            with open(config_path, 'r') as f:
                self.config = json.load(f)
        else:
            self.config = self._default_config()
        
        # Initialize components
        self.jobs = []
        self.plugins = []
        
    def _default_config(self) -> Dict[str, Any]:
        """Return default configuration"""
        return {
            "version": "2.2.0",
            "branding": {
                "author": "RAJSARASWATI JATAV",
                "watermark": "© RAJSARASWATI JATAV 2025"
            },
            "defaults": {
                "video_codec": "libx264",
                "audio_codec": "aac",
                "quality": "high",
                "parallel_jobs": 4
            }
        }
    
    def batch_convert(
        self,
        input_dir: str,
        output_dir: str,
        format: str = "mp4",
        ai_upscale: Optional[str] = None,
        enhance: bool = False,
        watermark: Optional[str] = None,
        logo: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Batch convert videos with optional AI enhancement
        
        Args:
            input_dir: Input directory path
            output_dir: Output directory path
            format: Output format (mp4, avi, mkv, etc.)
            ai_upscale: AI upscale factor (2x, 4x, 8x)
            enhance: Apply AI enhancement
            watermark: Watermark text
            logo: Logo image path
            
        Returns:
            Processing report
        """
        os.makedirs(output_dir, exist_ok=True)
        
        # Find all video files
        video_extensions = ['.mp4', '.avi', '.mkv', '.mov', '.flv', '.wmv']
        input_path = Path(input_dir)
        video_files = []
        
        for ext in video_extensions:
            video_files.extend(input_path.glob(f'*{ext}'))
        
        results = []
        for video_file in video_files:
            output_file = Path(output_dir) / f"{video_file.stem}_converted.{format}"
            
            # Build FFmpeg command
            cmd = self._build_convert_command(
                str(video_file),
                str(output_file),
                ai_upscale=ai_upscale,
                enhance=enhance,
                watermark=watermark,
                logo=logo,
                **kwargs
            )
            
            # Execute conversion
            result = self._execute_ffmpeg(cmd, str(video_file), str(output_file))
            results.append(result)
        
        return {
            "toolkit": "RSJ-FFMPEG",
            "version": self.version,
            "processed_by": self.author,
            "timestamp": datetime.now().isoformat(),
            "jobs": results,
            "summary": {
                "total_jobs": len(results),
                "completed": sum(1 for r in results if r["status"] == "completed"),
                "failed": sum(1 for r in results if r["status"] == "failed")
            }
        }
    
    def _build_convert_command(
        self,
        input_file: str,
        output_file: str,
        ai_upscale: Optional[str] = None,
        enhance: bool = False,
        watermark: Optional[str] = None,
        logo: Optional[str] = None,
        **kwargs
    ) -> List[str]:
        """Build FFmpeg command with all options"""
        cmd = ["ffmpeg", "-i", input_file]
        
        # Video filters
        filters = []
        
        # AI Upscaling (simulated - would use Real-ESRGAN in production)
        if ai_upscale:
            scale_factor = ai_upscale.replace('x', '')
            filters.append(f"scale=iw*{scale_factor}:ih*{scale_factor}:flags=lanczos")
        
        # Enhancement
        if enhance:
            filters.append("eq=contrast=1.1:brightness=0.05:saturation=1.2")
            filters.append("unsharp=5:5:1.0:5:5:0.0")
        
        # Watermark
        if watermark:
            # Text watermark
            watermark_filter = f"drawtext=text='{watermark}':fontsize=24:fontcolor=white@0.7:x=10:y=H-th-10"
            filters.append(watermark_filter)
        
        # Logo overlay
        if logo and os.path.exists(logo):
            filters.append(f"movie={logo}[logo];[in][logo]overlay=W-w-10:10[out]")
        
        # Apply filters
        if filters:
            cmd.extend(["-vf", ",".join(filters)])
        
        # Codec settings
        cmd.extend([
            "-c:v", self.config["defaults"]["video_codec"],
            "-c:a", self.config["defaults"]["audio_codec"],
            "-crf", "18",  # High quality
            "-preset", "medium"
        ])
        
        cmd.append(output_file)
        return cmd
    
    def _execute_ffmpeg(self, cmd: List[str], input_file: str, output_file: str) -> Dict[str, Any]:
        """Execute FFmpeg command and return result"""
        start_time = datetime.now()
        
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=3600  # 1 hour timeout
            )
            
            status = "completed" if result.returncode == 0 else "failed"
            duration = (datetime.now() - start_time).total_seconds()
            
            # Get file sizes
            input_size = os.path.getsize(input_file) if os.path.exists(input_file) else 0
            output_size = os.path.getsize(output_file) if os.path.exists(output_file) else 0
            
            return {
                "input": os.path.basename(input_file),
                "output": os.path.basename(output_file),
                "status": status,
                "duration": f"{duration:.1f}s",
                "file_size": {
                    "input": f"{input_size / (1024*1024):.1f}MB",
                    "output": f"{output_size / (1024*1024):.1f}MB"
                }
            }
        except Exception as e:
            return {
                "input": os.path.basename(input_file),
                "output": os.path.basename(output_file),
                "status": "failed",
                "error": str(e)
            }
    
    def ai_enhance(
        self,
        input_file: str,
        output_file: str,
        upscale: int = 2,
        denoise: bool = True,
        colorize: bool = False,
        stabilize: bool = False
    ) -> Dict[str, Any]:
        """
        AI-powered video enhancement
        
        Args:
            input_file: Input video path
            output_file: Output video path
            upscale: Upscale factor (2, 4, 8)
            denoise: Apply AI denoising
            colorize: Apply AI colorization
            stabilize: Apply AI stabilization
            
        Returns:
            Processing result
        """
        filters = []
        
        # Upscaling
        if upscale > 1:
            filters.append(f"scale=iw*{upscale}:ih*{upscale}:flags=lanczos")
        
        # Denoising
        if denoise:
            filters.append("hqdn3d=4:3:6:4.5")
        
        # Colorization (basic color enhancement)
        if colorize:
            filters.append("eq=contrast=1.2:brightness=0.1:saturation=1.3")
        
        # Stabilization
        if stabilize:
            filters.append("deshake")
        
        cmd = ["ffmpeg", "-i", input_file]
        if filters:
            cmd.extend(["-vf", ",".join(filters)])
        
        cmd.extend([
            "-c:v", "libx264",
            "-crf", "18",
            "-preset", "slow",
            output_file
        ])
        
        return self._execute_ffmpeg(cmd, input_file, output_file)
    
    def start_stream(
        self,
        platform: str,
        key: str,
        input_source: str = "webcam",
        overlay: Optional[str] = None,
        stats: bool = False,
        telegram_bot: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Start live streaming
        
        Args:
            platform: Streaming platform (youtube, twitch, facebook, etc.)
            key: Stream key
            input_source: Input source (webcam, screen, file)
            overlay: Overlay image path
            stats: Show stats overlay
            telegram_bot: Telegram bot token for control
            
        Returns:
            Stream information
        """
        # Platform RTMP URLs
        rtmp_urls = {
            "youtube": f"rtmp://a.rtmp.youtube.com/live2/{key}",
            "twitch": f"rtmp://live.twitch.tv/app/{key}",
            "facebook": f"rtmps://live-api-s.facebook.com:443/rtmp/{key}"
        }
        
        stream_url = rtmp_urls.get(platform, key)
        
        # Build streaming command
        cmd = ["ffmpeg"]
        
        # Input source
        if input_source == "webcam":
            cmd.extend(["-f", "v4l2", "-i", "/dev/video0"])
        elif input_source == "screen":
            cmd.extend(["-f", "x11grab", "-i", ":0.0"])
        else:
            cmd.extend(["-re", "-i", input_source])
        
        # Filters
        filters = []
        if overlay and os.path.exists(overlay):
            filters.append(f"movie={overlay}[logo];[in][logo]overlay=W-w-10:10[out]")
        
        if stats:
            filters.append("drawtext=text='LIVE - RSJ':fontsize=32:fontcolor=red:x=10:y=10")
        
        if filters:
            cmd.extend(["-vf", ",".join(filters)])
        
        # Streaming settings
        cmd.extend([
            "-c:v", "libx264",
            "-preset", "veryfast",
            "-maxrate", "3000k",
            "-bufsize", "6000k",
            "-pix_fmt", "yuv420p",
            "-g", "50",
            "-c:a", "aac",
            "-b:a", "128k",
            "-ar", "44100",
            "-f", "flv",
            stream_url
        ])
        
        return {
            "platform": platform,
            "stream_url": stream_url,
            "command": " ".join(cmd),
            "status": "ready"
        }
    
    def extract_audio(self, input_file: str, output_file: str, format: str = "mp3") -> Dict[str, Any]:
        """Extract audio from video"""
        cmd = [
            "ffmpeg", "-i", input_file,
            "-vn",  # No video
            "-acodec", "libmp3lame" if format == "mp3" else "copy",
            "-ab", "320k",
            output_file
        ]
        return self._execute_ffmpeg(cmd, input_file, output_file)
    
    def create_gif(
        self,
        input_file: str,
        output_file: str,
        start_time: str = "00:00:00",
        duration: int = 5,
        fps: int = 10,
        width: int = 480
    ) -> Dict[str, Any]:
        """Create optimized GIF from video"""
        # Generate palette for better quality
        palette_file = "palette.png"
        
        # Generate palette
        palette_cmd = [
            "ffmpeg", "-i", input_file,
            "-ss", start_time,
            "-t", str(duration),
            "-vf", f"fps={fps},scale={width}:-1:flags=lanczos,palettegen",
            "-y", palette_file
        ]
        subprocess.run(palette_cmd, capture_output=True)
        
        # Create GIF using palette
        cmd = [
            "ffmpeg", "-i", input_file,
            "-i", palette_file,
            "-ss", start_time,
            "-t", str(duration),
            "-filter_complex", f"fps={fps},scale={width}:-1:flags=lanczos[x];[x][1:v]paletteuse",
            "-y", output_file
        ]
        
        result = self._execute_ffmpeg(cmd, input_file, output_file)
        
        # Cleanup palette
        if os.path.exists(palette_file):
            os.remove(palette_file)
        
        return result
    
    def add_watermark(
        self,
        input_file: str,
        output_file: str,
        watermark_text: str,
        position: str = "bottom-right",
        opacity: float = 0.7
    ) -> Dict[str, Any]:
        """Add text watermark to video"""
        # Position mapping
        positions = {
            "top-left": "x=10:y=10",
            "top-right": "x=W-tw-10:y=10",
            "bottom-left": "x=10:y=H-th-10",
            "bottom-right": "x=W-tw-10:y=H-th-10",
            "center": "x=(W-tw)/2:y=(H-th)/2"
        }
        
        pos = positions.get(position, positions["bottom-right"])
        
        cmd = [
            "ffmpeg", "-i", input_file,
            "-vf", f"drawtext=text='{watermark_text}':fontsize=24:fontcolor=white@{opacity}:{pos}",
            "-codec:a", "copy",
            output_file
        ]
        
        return self._execute_ffmpeg(cmd, input_file, output_file)
    
    def get_video_info(self, input_file: str) -> Dict[str, Any]:
        """Get video information using ffprobe"""
        cmd = [
            "ffprobe",
            "-v", "quiet",
            "-print_format", "json",
            "-show_format",
            "-show_streams",
            input_file
        ]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True)
            return json.loads(result.stdout)
        except Exception as e:
            return {"error": str(e)}