"""
RSJ-FFMPEG Audio Processing Module
Advanced audio manipulation and AI separation
"""

import subprocess
from typing import Optional, List, Dict, Any
from pathlib import Path


class AudioProcessor:
    """Advanced audio processing capabilities"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
    
    def normalize_audio(
        self,
        input_file: str,
        output_file: str,
        target_level: float = -23.0
    ) -> Dict[str, Any]:
        """
        Normalize audio to target loudness level
        
        Args:
            input_file: Input audio/video file
            output_file: Output file
            target_level: Target LUFS level (default: -23.0)
        """
        cmd = [
            "ffmpeg", "-i", input_file,
            "-af", f"loudnorm=I={target_level}:TP=-1.5:LRA=11",
            "-c:v", "copy",
            output_file
        ]
        
        try:
            subprocess.run(cmd, check=True, capture_output=True)
            return {"status": "success", "target_level": target_level}
        except subprocess.CalledProcessError as e:
            return {"status": "failed", "error": str(e)}
    
    def apply_audio_effects(
        self,
        input_file: str,
        output_file: str,
        effects: List[str]
    ) -> Dict[str, Any]:
        """
        Apply audio effects (reverb, echo, compression, eq)
        
        Args:
            input_file: Input file
            output_file: Output file
            effects: List of effects to apply
        """
        filters = []
        
        for effect in effects:
            if effect == "reverb":
                filters.append("aecho=0.8:0.9:1000:0.3")
            elif effect == "echo":
                filters.append("aecho=0.8:0.88:60:0.4")
            elif effect == "compression":
                filters.append("acompressor=threshold=0.089:ratio=9:attack=200:release=1000")
            elif effect == "eq":
                filters.append("equalizer=f=1000:width_type=h:width=200:g=5")
            elif effect == "bass_boost":
                filters.append("bass=g=10:f=110:w=0.3")
            elif effect == "treble_boost":
                filters.append("treble=g=5:f=5000:w=0.5")
        
        if not filters:
            return {"status": "failed", "error": "No valid effects specified"}
        
        cmd = [
            "ffmpeg", "-i", input_file,
            "-af", ",".join(filters),
            "-c:v", "copy",
            output_file
        ]
        
        try:
            subprocess.run(cmd, check=True, capture_output=True)
            return {"status": "success", "effects": effects}
        except subprocess.CalledProcessError as e:
            return {"status": "failed", "error": str(e)}
    
    def extract_channels(
        self,
        input_file: str,
        output_dir: str
    ) -> Dict[str, Any]:
        """Extract individual audio channels"""
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        
        # Extract left channel
        cmd_left = [
            "ffmpeg", "-i", input_file,
            "-af", "pan=mono|c0=FL",
            f"{output_dir}/left_channel.wav"
        ]
        
        # Extract right channel
        cmd_right = [
            "ffmpeg", "-i", input_file,
            "-af", "pan=mono|c0=FR",
            f"{output_dir}/right_channel.wav"
        ]
        
        try:
            subprocess.run(cmd_left, check=True, capture_output=True)
            subprocess.run(cmd_right, check=True, capture_output=True)
            return {"status": "success", "output_dir": output_dir}
        except subprocess.CalledProcessError as e:
            return {"status": "failed", "error": str(e)}
    
    def merge_audio_video(
        self,
        video_file: str,
        audio_file: str,
        output_file: str
    ) -> Dict[str, Any]:
        """Merge separate audio and video files"""
        cmd = [
            "ffmpeg",
            "-i", video_file,
            "-i", audio_file,
            "-c:v", "copy",
            "-c:a", "aac",
            "-map", "0:v:0",
            "-map", "1:a:0",
            output_file
        ]
        
        try:
            subprocess.run(cmd, check=True, capture_output=True)
            return {"status": "success"}
        except subprocess.CalledProcessError as e:
            return {"status": "failed", "error": str(e)}
    
    def change_audio_speed(
        self,
        input_file: str,
        output_file: str,
        speed: float = 1.0
    ) -> Dict[str, Any]:
        """Change audio playback speed without changing pitch"""
        # atempo filter has limits, chain for extreme speeds
        atempo_filters = []
        atempo = speed
        
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
            "-af", ",".join(atempo_filters),
            output_file
        ]
        
        try:
            subprocess.run(cmd, check=True, capture_output=True)
            return {"status": "success", "speed": speed}
        except subprocess.CalledProcessError as e:
            return {"status": "failed", "error": str(e)}
    
    def remove_silence(
        self,
        input_file: str,
        output_file: str,
        noise_threshold: float = -50.0,
        duration: float = 0.5
    ) -> Dict[str, Any]:
        """Remove silence from audio"""
        cmd = [
            "ffmpeg", "-i", input_file,
            "-af", f"silenceremove=start_periods=1:start_duration={duration}:start_threshold={noise_threshold}dB:detection=peak,aformat=dblp,areverse,silenceremove=start_periods=1:start_duration={duration}:start_threshold={noise_threshold}dB:detection=peak,aformat=dblp,areverse",
            output_file
        ]
        
        try:
            subprocess.run(cmd, check=True, capture_output=True)
            return {"status": "success"}
        except subprocess.CalledProcessError as e:
            return {"status": "failed", "error": str(e)}
    
    def create_waveform_video(
        self,
        audio_file: str,
        output_file: str,
        background: Optional[str] = None,
        width: int = 1920,
        height: int = 1080
    ) -> Dict[str, Any]:
        """Create waveform visualization video from audio"""
        filters = []
        
        if background:
            # Use background image
            filters.append(f"movie={background}[bg];")
            filters.append("[0:a]showwaves=s={width}x{height}:mode=line:colors=cyan[waves];")
            filters.append("[bg][waves]overlay[out]")
        else:
            # Black background
            filters.append(f"[0:a]showwaves=s={width}x{height}:mode=line:colors=cyan[out]")
        
        cmd = [
            "ffmpeg", "-i", audio_file,
            "-filter_complex", "".join(filters),
            "-map", "[out]",
            "-map", "0:a",
            "-c:v", "libx264",
            "-c:a", "copy",
            "-pix_fmt", "yuv420p",
            output_file
        ]
        
        try:
            subprocess.run(cmd, check=True, capture_output=True)
            return {"status": "success"}
        except subprocess.CalledProcessError as e:
            return {"status": "failed", "error": str(e)}
    
    def create_spectrum_video(
        self,
        audio_file: str,
        output_file: str,
        width: int = 1920,
        height: int = 1080
    ) -> Dict[str, Any]:
        """Create spectrum analyzer visualization"""
        cmd = [
            "ffmpeg", "-i", audio_file,
            "-filter_complex",
            f"[0:a]showspectrum=s={width}x{height}:mode=combined:color=rainbow:scale=log[out]",
            "-map", "[out]",
            "-map", "0:a",
            "-c:v", "libx264",
            "-c:a", "copy",
            "-pix_fmt", "yuv420p",
            output_file
        ]
        
        try:
            subprocess.run(cmd, check=True, capture_output=True)
            return {"status": "success"}
        except subprocess.CalledProcessError as e:
            return {"status": "failed", "error": str(e)}