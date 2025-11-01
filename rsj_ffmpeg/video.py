"""
RSJ-FFMPEG Video Processing Module
Advanced video manipulation and enhancement
"""

import subprocess
from typing import Optional, List, Dict, Any
from pathlib import Path


class VideoProcessor:
    """Advanced video processing capabilities"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
    
    def extract_frames(
        self,
        input_file: str,
        output_dir: str,
        fps: int = 1,
        format: str = "png",
        start_time: Optional[str] = None,
        duration: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Extract frames from video
        
        Args:
            input_file: Input video path
            output_dir: Output directory for frames
            fps: Frames per second to extract
            format: Output format (png, jpg)
            start_time: Start time (HH:MM:SS)
            duration: Duration in seconds
        """
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        
        cmd = ["ffmpeg", "-i", input_file]
        
        if start_time:
            cmd.extend(["-ss", start_time])
        if duration:
            cmd.extend(["-t", str(duration)])
        
        cmd.extend([
            "-vf", f"fps={fps}",
            f"{output_dir}/frame_%04d.{format}"
        ])
        
        try:
            subprocess.run(cmd, check=True, capture_output=True)
            return {"status": "success", "output_dir": output_dir}
        except subprocess.CalledProcessError as e:
            return {"status": "failed", "error": str(e)}
    
    def create_thumbnail(
        self,
        input_file: str,
        output_file: str,
        timestamp: str = "00:00:01",
        width: int = 1280
    ) -> Dict[str, Any]:
        """Create thumbnail from video at specific timestamp"""
        cmd = [
            "ffmpeg", "-i", input_file,
            "-ss", timestamp,
            "-vframes", "1",
            "-vf", f"scale={width}:-1",
            output_file
        ]
        
        try:
            subprocess.run(cmd, check=True, capture_output=True)
            return {"status": "success", "thumbnail": output_file}
        except subprocess.CalledProcessError as e:
            return {"status": "failed", "error": str(e)}
    
    def change_speed(
        self,
        input_file: str,
        output_file: str,
        speed: float = 1.0
    ) -> Dict[str, Any]:
        """
        Change video playback speed
        
        Args:
            input_file: Input video
            output_file: Output video
            speed: Speed multiplier (0.5 = half speed, 2.0 = double speed)
        """
        # Calculate PTS (presentation timestamp) multiplier
        pts = 1.0 / speed
        
        # Audio tempo adjustment
        atempo = speed
        
        # FFmpeg has atempo limits, need to chain for extreme speeds
        atempo_filters = []
        while atempo > 2.0:
            atempo_filters.append("atempo=2.0")
            atempo /= 2.0
        while atempo < 0.5:
            atempo_filters.append("atempo=0.5")
            atempo *= 2.0
        if atempo != 1.0:
            atempo_filters.append(f"atempo={atempo}")
        
        cmd = [
            "ffmpeg", "-i", input_file,
            "-filter_complex",
            f"[0:v]setpts={pts}*PTS[v];[0:a]{','.join(atempo_filters)}[a]",
            "-map", "[v]",
            "-map", "[a]",
            output_file
        ]
        
        try:
            subprocess.run(cmd, check=True, capture_output=True)
            return {"status": "success", "speed": speed}
        except subprocess.CalledProcessError as e:
            return {"status": "failed", "error": str(e)}
    
    def concatenate_videos(
        self,
        input_files: List[str],
        output_file: str
    ) -> Dict[str, Any]:
        """Concatenate multiple videos"""
        # Create concat file
        concat_file = "concat_list.txt"
        with open(concat_file, 'w') as f:
            for video in input_files:
                f.write(f"file '{video}'\n")
        
        cmd = [
            "ffmpeg",
            "-f", "concat",
            "-safe", "0",
            "-i", concat_file,
            "-c", "copy",
            output_file
        ]
        
        try:
            subprocess.run(cmd, check=True, capture_output=True)
            return {"status": "success", "output": output_file}
        finally:
            if Path(concat_file).exists():
                Path(concat_file).unlink()
    
    def trim_video(
        self,
        input_file: str,
        output_file: str,
        start_time: str,
        end_time: str
    ) -> Dict[str, Any]:
        """Trim video to specific time range"""
        cmd = [
            "ffmpeg", "-i", input_file,
            "-ss", start_time,
            "-to", end_time,
            "-c", "copy",
            output_file
        ]
        
        try:
            subprocess.run(cmd, check=True, capture_output=True)
            return {"status": "success"}
        except subprocess.CalledProcessError as e:
            return {"status": "failed", "error": str(e)}
    
    def add_intro_outro(
        self,
        input_file: str,
        output_file: str,
        intro_file: Optional[str] = None,
        outro_file: Optional[str] = None
    ) -> Dict[str, Any]:
        """Add intro and/or outro to video"""
        files_to_concat = []
        
        if intro_file:
            files_to_concat.append(intro_file)
        files_to_concat.append(input_file)
        if outro_file:
            files_to_concat.append(outro_file)
        
        return self.concatenate_videos(files_to_concat, output_file)
    
    def apply_lut(
        self,
        input_file: str,
        output_file: str,
        lut_file: str
    ) -> Dict[str, Any]:
        """Apply color LUT (Look-Up Table) to video"""
        cmd = [
            "ffmpeg", "-i", input_file,
            "-vf", f"lut3d={lut_file}",
            "-c:a", "copy",
            output_file
        ]
        
        try:
            subprocess.run(cmd, check=True, capture_output=True)
            return {"status": "success"}
        except subprocess.CalledProcessError as e:
            return {"status": "failed", "error": str(e)}
    
    def stabilize_video(
        self,
        input_file: str,
        output_file: str
    ) -> Dict[str, Any]:
        """Stabilize shaky video"""
        # Two-pass stabilization
        # Pass 1: Analyze
        trf_file = "transforms.trf"
        cmd1 = [
            "ffmpeg", "-i", input_file,
            "-vf", f"vidstabdetect=shakiness=10:accuracy=15:result={trf_file}",
            "-f", "null", "-"
        ]
        
        try:
            subprocess.run(cmd1, check=True, capture_output=True)
            
            # Pass 2: Transform
            cmd2 = [
                "ffmpeg", "-i", input_file,
                "-vf", f"vidstabtransform=input={trf_file}:zoom=0:smoothing=10",
                "-c:a", "copy",
                output_file
            ]
            subprocess.run(cmd2, check=True, capture_output=True)
            
            return {"status": "success"}
        except subprocess.CalledProcessError as e:
            return {"status": "failed", "error": str(e)}
        finally:
            if Path(trf_file).exists():
                Path(trf_file).unlink()