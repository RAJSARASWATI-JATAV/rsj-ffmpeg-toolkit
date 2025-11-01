"""
RSJ-FFMPEG Video Templates
Pre-built templates for common video types

Author: RAJSARASWATI JATAV
Version: 2.2.0
"""

import subprocess
from typing import Dict, Any, List, Optional
from pathlib import Path
import json


class VideoTemplates:
    """Pre-built video templates"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.templates = self._load_templates()
    
    def _load_templates(self) -> Dict[str, Any]:
        """Load template definitions"""
        return {
            "youtube_intro": {
                "duration": 5,
                "resolution": "1920x1080",
                "fps": 30,
                "elements": ["logo", "title", "subscribe_button"]
            },
            "youtube_outro": {
                "duration": 10,
                "resolution": "1920x1080",
                "fps": 30,
                "elements": ["end_screen", "subscribe", "next_video"]
            },
            "instagram_story": {
                "duration": 15,
                "resolution": "1080x1920",
                "fps": 30,
                "elements": ["text_overlay", "stickers"]
            },
            "instagram_reel": {
                "duration": 30,
                "resolution": "1080x1920",
                "fps": 30,
                "elements": ["captions", "music"]
            },
            "tiktok_video": {
                "duration": 60,
                "resolution": "1080x1920",
                "fps": 30,
                "elements": ["effects", "text", "music"]
            },
            "linkedin_post": {
                "duration": 120,
                "resolution": "1920x1080",
                "fps": 30,
                "elements": ["professional_title", "captions"]
            },
            "facebook_ad": {
                "duration": 15,
                "resolution": "1080x1080",
                "fps": 30,
                "elements": ["cta_button", "brand_logo"]
            },
            "twitter_video": {
                "duration": 140,
                "resolution": "1280x720",
                "fps": 30,
                "elements": ["captions"]
            }
        }
    
    def create_youtube_intro(
        self,
        output: str,
        title: str,
        logo: Optional[str] = None,
        background: Optional[str] = None,
        music: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Create YouTube intro
        
        Args:
            output: Output file path
            title: Channel/video title
            logo: Logo image path
            background: Background video/image
            music: Background music
            
        Returns:
            Creation result
        """
        try:
            # Create intro with title animation
            cmd = [
                "ffmpeg",
                "-f", "lavfi",
                "-i", "color=c=black:s=1920x1080:d=5",
                "-vf", f"drawtext=text='{title}':fontsize=72:fontcolor=white:x=(w-text_w)/2:y=(h-text_h)/2:enable='between(t,1,4)'",
                "-c:v", "libx264",
                "-t", "5",
                "-pix_fmt", "yuv420p"
            ]
            
            # Add music if provided
            if music:
                cmd.extend(["-i", music, "-c:a", "aac", "-shortest"])
            
            cmd.extend(["-y", output])
            
            subprocess.run(cmd, check=True, capture_output=True)
            
            return {
                "status": "success",
                "output": output,
                "template": "youtube_intro"
            }
            
        except Exception as e:
            return {"status": "failed", "error": str(e)}
    
    def create_youtube_outro(
        self,
        output: str,
        channel_name: str,
        subscribe_text: str = "Subscribe for more!",
        end_screen: Optional[str] = None
    ) -> Dict[str, Any]:
        """Create YouTube outro with end screen"""
        try:
            cmd = [
                "ffmpeg",
                "-f", "lavfi",
                "-i", "color=c=#1a1a1a:s=1920x1080:d=10",
                "-vf", f"drawtext=text='{channel_name}':fontsize=64:fontcolor=white:x=(w-text_w)/2:y=200,"
                       f"drawtext=text='{subscribe_text}':fontsize=48:fontcolor=red:x=(w-text_w)/2:y=600",
                "-c:v", "libx264",
                "-t", "10",
                "-pix_fmt", "yuv420p",
                "-y", output
            ]
            
            subprocess.run(cmd, check=True, capture_output=True)
            
            return {
                "status": "success",
                "output": output,
                "template": "youtube_outro"
            }
            
        except Exception as e:
            return {"status": "failed", "error": str(e)}
    
    def create_instagram_story(
        self,
        input_video: str,
        output: str,
        text_overlay: Optional[str] = None,
        stickers: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """Create Instagram story format"""
        try:
            # Resize to 1080x1920 (9:16)
            filters = ["scale=1080:1920:force_original_aspect_ratio=decrease",
                      "pad=1080:1920:(ow-iw)/2:(oh-ih)/2"]
            
            if text_overlay:
                filters.append(
                    f"drawtext=text='{text_overlay}':fontsize=48:fontcolor=white:"
                    f"x=(w-text_w)/2:y=100:box=1:boxcolor=black@0.5:boxborderw=10"
                )
            
            cmd = [
                "ffmpeg", "-i", input_video,
                "-vf", ",".join(filters),
                "-c:v", "libx264",
                "-c:a", "aac",
                "-t", "15",
                "-y", output
            ]
            
            subprocess.run(cmd, check=True, capture_output=True)
            
            return {
                "status": "success",
                "output": output,
                "template": "instagram_story"
            }
            
        except Exception as e:
            return {"status": "failed", "error": str(e)}
    
    def create_instagram_reel(
        self,
        input_video: str,
        output: str,
        captions: Optional[List[Dict[str, str]]] = None,
        music: Optional[str] = None
    ) -> Dict[str, Any]:
        """Create Instagram Reel"""
        try:
            filters = [
                "scale=1080:1920:force_original_aspect_ratio=decrease",
                "pad=1080:1920:(ow-iw)/2:(oh-ih)/2"
            ]
            
            cmd = [
                "ffmpeg", "-i", input_video,
                "-vf", ",".join(filters),
                "-c:v", "libx264",
                "-c:a", "aac",
                "-t", "30",
                "-y", output
            ]
            
            if music:
                cmd = [
                    "ffmpeg", "-i", input_video, "-i", music,
                    "-vf", ",".join(filters),
                    "-c:v", "libx264",
                    "-c:a", "aac",
                    "-shortest",
                    "-y", output
                ]
            
            subprocess.run(cmd, check=True, capture_output=True)
            
            return {
                "status": "success",
                "output": output,
                "template": "instagram_reel"
            }
            
        except Exception as e:
            return {"status": "failed", "error": str(e)}
    
    def create_tiktok_video(
        self,
        input_video: str,
        output: str,
        effects: Optional[List[str]] = None,
        text: Optional[str] = None
    ) -> Dict[str, Any]:
        """Create TikTok format video"""
        try:
            filters = [
                "scale=1080:1920:force_original_aspect_ratio=decrease",
                "pad=1080:1920:(ow-iw)/2:(oh-ih)/2"
            ]
            
            if text:
                filters.append(
                    f"drawtext=text='{text}':fontsize=56:fontcolor=white:"
                    f"x=(w-text_w)/2:y=h-150:box=1:boxcolor=black@0.7:boxborderw=10"
                )
            
            cmd = [
                "ffmpeg", "-i", input_video,
                "-vf", ",".join(filters),
                "-c:v", "libx264",
                "-c:a", "aac",
                "-t", "60",
                "-y", output
            ]
            
            subprocess.run(cmd, check=True, capture_output=True)
            
            return {
                "status": "success",
                "output": output,
                "template": "tiktok_video"
            }
            
        except Exception as e:
            return {"status": "failed", "error": str(e)}
    
    def create_linkedin_post(
        self,
        input_video: str,
        output: str,
        title: str,
        captions: bool = True
    ) -> Dict[str, Any]:
        """Create LinkedIn post video"""
        try:
            filters = [
                "scale=1920:1080:force_original_aspect_ratio=decrease",
                "pad=1920:1080:(ow-iw)/2:(oh-ih)/2"
            ]
            
            filters.append(
                f"drawtext=text='{title}':fontsize=48:fontcolor=white:"
                f"x=50:y=50:box=1:boxcolor=blue@0.8:boxborderw=10"
            )
            
            cmd = [
                "ffmpeg", "-i", input_video,
                "-vf", ",".join(filters),
                "-c:v", "libx264",
                "-c:a", "aac",
                "-t", "120",
                "-y", output
            ]
            
            subprocess.run(cmd, check=True, capture_output=True)
            
            return {
                "status": "success",
                "output": output,
                "template": "linkedin_post"
            }
            
        except Exception as e:
            return {"status": "failed", "error": str(e)}
    
    def create_facebook_ad(
        self,
        input_video: str,
        output: str,
        cta_text: str = "Learn More",
        logo: Optional[str] = None
    ) -> Dict[str, Any]:
        """Create Facebook ad video"""
        try:
            # Square format 1:1
            filters = [
                "scale=1080:1080:force_original_aspect_ratio=decrease",
                "pad=1080:1080:(ow-iw)/2:(oh-ih)/2"
            ]
            
            # Add CTA button
            filters.append(
                f"drawtext=text='{cta_text}':fontsize=40:fontcolor=white:"
                f"x=(w-text_w)/2:y=h-100:box=1:boxcolor=green@0.9:boxborderw=15"
            )
            
            cmd = [
                "ffmpeg", "-i", input_video,
                "-vf", ",".join(filters),
                "-c:v", "libx264",
                "-c:a", "aac",
                "-t", "15",
                "-y", output
            ]
            
            subprocess.run(cmd, check=True, capture_output=True)
            
            return {
                "status": "success",
                "output": output,
                "template": "facebook_ad"
            }
            
        except Exception as e:
            return {"status": "failed", "error": str(e)}
    
    def get_template_info(self, template_name: str) -> Optional[Dict[str, Any]]:
        """Get template information"""
        return self.templates.get(template_name)
    
    def list_templates(self) -> List[str]:
        """List available templates"""
        return list(self.templates.keys())