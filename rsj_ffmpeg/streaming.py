"""
RSJ-FFMPEG Streaming Module
Live streaming capabilities for multiple platforms
"""

import subprocess
import threading
import time
from typing import Optional, Dict, Any, List
from datetime import datetime


class StreamManager:
    """Manage live streaming operations"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.active_streams = {}
        self.stream_stats = {}
        
    def get_rtmp_url(self, platform: str, key: str) -> str:
        """Get RTMP URL for platform"""
        urls = {
            "youtube": f"rtmp://a.rtmp.youtube.com/live2/{key}",
            "twitch": f"rtmp://live.twitch.tv/app/{key}",
            "facebook": f"rtmps://live-api-s.facebook.com:443/rtmp/{key}",
            "instagram": f"rtmps://live-upload.instagram.com:443/rtmp/{key}",
            "custom": key  # Direct RTMP URL
        }
        return urls.get(platform, key)
    
    def build_stream_command(
        self,
        input_source: str,
        stream_url: str,
        overlay: Optional[str] = None,
        stats_overlay: bool = False,
        chat_overlay: Optional[str] = None,
        watermark: Optional[str] = None,
        bitrate: str = "3000k",
        fps: int = 30,
        resolution: str = "1920x1080"
    ) -> List[str]:
        """Build FFmpeg streaming command"""
        cmd = ["ffmpeg"]
        
        # Input source
        if input_source == "webcam":
            # Linux/Mac
            cmd.extend(["-f", "v4l2", "-i", "/dev/video0"])
        elif input_source == "screen":
            # Linux X11
            cmd.extend(["-f", "x11grab", "-i", ":0.0"])
        elif input_source == "desktop":
            # Alternative for screen capture
            cmd.extend(["-f", "gdigrab", "-i", "desktop"])
        elif input_source.startswith("rtsp://"):
            # RTSP camera stream
            cmd.extend(["-i", input_source])
        else:
            # File input with loop
            cmd.extend(["-re", "-stream_loop", "-1", "-i", input_source])
        
        # Video filters
        filters = []
        
        # Resolution scaling
        if resolution:
            filters.append(f"scale={resolution}")
        
        # Overlay image (logo/watermark)
        if overlay:
            filters.append(f"movie={overlay}[logo];[in][logo]overlay=W-w-10:10[out]")
        
        # Stats overlay
        if stats_overlay:
            timestamp = "%{localtime\\:%Y-%m-%d %H\\\\:%M\\\\:%S}"
            filters.append(f"drawtext=text='LIVE - RSJ':fontsize=32:fontcolor=red:x=10:y=10")
            filters.append(f"drawtext=text='{timestamp}':fontsize=20:fontcolor=white:x=10:y=50")
        
        # Watermark text
        if watermark:
            filters.append(f"drawtext=text='{watermark}':fontsize=24:fontcolor=white@0.7:x=W-tw-10:y=H-th-10")
        
        # Apply filters
        if filters:
            cmd.extend(["-vf", ",".join(filters)])
        
        # Video encoding settings
        cmd.extend([
            "-c:v", "libx264",
            "-preset", "veryfast",
            "-tune", "zerolatency",
            "-b:v", bitrate,
            "-maxrate", bitrate,
            "-bufsize", str(int(bitrate.replace('k', '')) * 2) + 'k',
            "-pix_fmt", "yuv420p",
            "-g", str(fps * 2),  # Keyframe interval
            "-r", str(fps)
        ])
        
        # Audio encoding
        cmd.extend([
            "-c:a", "aac",
            "-b:a", "128k",
            "-ar", "44100",
            "-ac", "2"
        ])
        
        # Output format
        cmd.extend([
            "-f", "flv",
            stream_url
        ])
        
        return cmd
    
    def start_stream(
        self,
        stream_id: str,
        platform: str,
        key: str,
        input_source: str = "webcam",
        **kwargs
    ) -> Dict[str, Any]:
        """Start a live stream"""
        stream_url = self.get_rtmp_url(platform, key)
        cmd = self.build_stream_command(input_source, stream_url, **kwargs)
        
        try:
            # Start streaming process
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True
            )
            
            self.active_streams[stream_id] = {
                "process": process,
                "platform": platform,
                "stream_url": stream_url,
                "start_time": datetime.now(),
                "command": " ".join(cmd)
            }
            
            self.stream_stats[stream_id] = {
                "status": "live",
                "start_time": datetime.now().isoformat(),
                "platform": platform
            }
            
            return {
                "status": "started",
                "stream_id": stream_id,
                "platform": platform,
                "command": " ".join(cmd)
            }
        except Exception as e:
            return {
                "status": "failed",
                "error": str(e)
            }
    
    def stop_stream(self, stream_id: str) -> Dict[str, Any]:
        """Stop a live stream"""
        if stream_id not in self.active_streams:
            return {"status": "failed", "error": "Stream not found"}
        
        stream = self.active_streams[stream_id]
        process = stream["process"]
        
        try:
            process.terminate()
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            process.kill()
        
        duration = (datetime.now() - stream["start_time"]).total_seconds()
        
        del self.active_streams[stream_id]
        self.stream_stats[stream_id]["status"] = "stopped"
        self.stream_stats[stream_id]["duration"] = f"{duration:.1f}s"
        
        return {
            "status": "stopped",
            "stream_id": stream_id,
            "duration": f"{duration:.1f}s"
        }
    
    def get_stream_status(self, stream_id: str) -> Dict[str, Any]:
        """Get stream status"""
        if stream_id not in self.active_streams:
            return {"status": "not_found"}
        
        stream = self.active_streams[stream_id]
        process = stream["process"]
        
        if process.poll() is None:
            duration = (datetime.now() - stream["start_time"]).total_seconds()
            return {
                "status": "live",
                "platform": stream["platform"],
                "duration": f"{duration:.1f}s",
                "uptime": duration
            }
        else:
            return {
                "status": "stopped",
                "return_code": process.returncode
            }
    
    def multi_stream(
        self,
        platforms: Dict[str, str],
        input_source: str = "webcam",
        **kwargs
    ) -> Dict[str, Any]:
        """Stream to multiple platforms simultaneously"""
        results = {}
        
        for platform, key in platforms.items():
            stream_id = f"{platform}_{int(time.time())}"
            result = self.start_stream(
                stream_id=stream_id,
                platform=platform,
                key=key,
                input_source=input_source,
                **kwargs
            )
            results[platform] = result
        
        return {
            "status": "multi_stream_started",
            "platforms": results
        }
    
    def record_stream(
        self,
        stream_id: str,
        output_file: str
    ) -> Dict[str, Any]:
        """Record stream while streaming"""
        if stream_id not in self.active_streams:
            return {"status": "failed", "error": "Stream not found"}
        
        # This would require tee-ing the stream
        # For now, return placeholder
        return {
            "status": "recording",
            "output": output_file,
            "note": "Recording functionality requires stream tee setup"
        }


class SRTStreamer:
    """SRT (Secure Reliable Transport) streaming"""
    
    def __init__(self):
        self.active_streams = {}
    
    def start_srt_stream(
        self,
        input_source: str,
        srt_url: str,
        latency: int = 1000,
        **kwargs
    ) -> Dict[str, Any]:
        """Start SRT stream with low latency"""
        cmd = [
            "ffmpeg",
            "-re", "-i", input_source,
            "-c:v", "libx264",
            "-preset", "ultrafast",
            "-tune", "zerolatency",
            "-c:a", "aac",
            "-f", "mpegts",
            f"{srt_url}?latency={latency}"
        ]
        
        try:
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            return {
                "status": "started",
                "srt_url": srt_url,
                "latency": latency
            }
        except Exception as e:
            return {"status": "failed", "error": str(e)}


class HLSStreamer:
    """HLS (HTTP Live Streaming) generator"""
    
    def __init__(self):
        self.active_streams = {}
    
    def start_hls_stream(
        self,
        input_source: str,
        output_dir: str,
        segment_time: int = 6,
        **kwargs
    ) -> Dict[str, Any]:
        """Generate HLS stream"""
        import os
        os.makedirs(output_dir, exist_ok=True)
        
        cmd = [
            "ffmpeg",
            "-re", "-i", input_source,
            "-c:v", "libx264",
            "-c:a", "aac",
            "-f", "hls",
            "-hls_time", str(segment_time),
            "-hls_list_size", "10",
            "-hls_flags", "delete_segments",
            f"{output_dir}/stream.m3u8"
        ]
        
        try:
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            return {
                "status": "started",
                "playlist": f"{output_dir}/stream.m3u8",
                "segment_time": segment_time
            }
        except Exception as e:
            return {"status": "failed", "error": str(e)}