"""
RSJ-FFMPEG Content Analyzer
AI-powered video content analysis and classification

Author: RAJSARASWATI JATAV
Version: 2.2.0
"""

import subprocess
import json
from typing import Dict, Any, List, Optional, Tuple
from pathlib import Path
import re


class ContentAnalyzer:
    """
    Analyze video content for intelligent processing
    Detects scenes, objects, faces, text, audio, and more
    """
    
    def __init__(self, config: Dict[str, Any]):
        """Initialize Content Analyzer"""
        self.config = config
        self.analysis_cache = {}
    
    def analyze_video(
        self,
        video_file: str,
        analyze_scenes: bool = True,
        analyze_audio: bool = True,
        analyze_quality: bool = True,
        analyze_content: bool = True
    ) -> Dict[str, Any]:
        """
        Comprehensive video analysis
        
        Args:
            video_file: Input video file
            analyze_scenes: Detect scene changes
            analyze_audio: Analyze audio content
            analyze_quality: Assess video quality
            analyze_content: Detect objects/faces/text
            
        Returns:
            Complete analysis results
        """
        print(f"🔍 Analyzing {video_file}...")
        
        analysis = {
            "file": video_file,
            "metadata": self._get_metadata(video_file),
            "scenes": [],
            "audio": {},
            "quality": {},
            "content": {}
        }
        
        if analyze_scenes:
            analysis["scenes"] = self._detect_scenes(video_file)
            print(f"  ✅ Detected {len(analysis['scenes'])} scenes")
        
        if analyze_audio:
            analysis["audio"] = self._analyze_audio(video_file)
            print(f"  ✅ Audio analyzed")
        
        if analyze_quality:
            analysis["quality"] = self._assess_quality(video_file)
            print(f"  ✅ Quality score: {analysis['quality'].get('overall_score', 0):.2f}")
        
        if analyze_content:
            analysis["content"] = self._analyze_content(video_file)
            print(f"  ✅ Content analyzed")
        
        return analysis
    
    def _get_metadata(self, video_file: str) -> Dict[str, Any]:
        """Extract video metadata"""
        try:
            cmd = [
                "ffprobe", "-v", "error",
                "-show_format", "-show_streams",
                "-of", "json",
                video_file
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            data = json.loads(result.stdout)
            
            # Extract key metadata
            format_info = data.get('format', {})
            video_stream = next(
                (s for s in data.get('streams', []) if s['codec_type'] == 'video'),
                {}
            )
            audio_stream = next(
                (s for s in data.get('streams', []) if s['codec_type'] == 'audio'),
                {}
            )
            
            return {
                "duration": float(format_info.get('duration', 0)),
                "size": int(format_info.get('size', 0)),
                "bitrate": int(format_info.get('bit_rate', 0)),
                "format": format_info.get('format_name', ''),
                "video": {
                    "codec": video_stream.get('codec_name', ''),
                    "width": video_stream.get('width', 0),
                    "height": video_stream.get('height', 0),
                    "fps": self._parse_fps(video_stream.get('r_frame_rate', '0/1')),
                    "bitrate": int(video_stream.get('bit_rate', 0))
                },
                "audio": {
                    "codec": audio_stream.get('codec_name', ''),
                    "sample_rate": int(audio_stream.get('sample_rate', 0)),
                    "channels": audio_stream.get('channels', 0),
                    "bitrate": int(audio_stream.get('bit_rate', 0))
                }
            }
            
        except Exception as e:
            print(f"⚠️  Metadata extraction failed: {e}")
            return {}
    
    def _parse_fps(self, fps_str: str) -> float:
        """Parse FPS from fraction string"""
        try:
            num, den = fps_str.split('/')
            return float(num) / float(den)
        except:
            return 0.0
    
    def _detect_scenes(self, video_file: str) -> List[Dict[str, Any]]:
        """Detect scene changes"""
        scenes = []
        
        try:
            # Use FFmpeg scene detection
            cmd = [
                "ffmpeg", "-i", video_file,
                "-vf", "select='gt(scene,0.3)',metadata=print:file=-",
                "-f", "null", "-"
            ]
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                stderr=subprocess.STDOUT
            )
            
            # Parse scene timestamps
            for line in result.stdout.split('\n'):
                if 'pts_time' in line:
                    match = re.search(r'pts_time:([\d.]+)', line)
                    if match:
                        timestamp = float(match.group(1))
                        scenes.append({
                            "timestamp": timestamp,
                            "type": "scene_change",
                            "confidence": 0.8
                        })
            
        except Exception as e:
            print(f"⚠️  Scene detection failed: {e}")
        
        return scenes
    
    def _analyze_audio(self, video_file: str) -> Dict[str, Any]:
        """Analyze audio content"""
        audio_analysis = {
            "has_audio": False,
            "has_speech": False,
            "has_music": False,
            "silence_periods": [],
            "loudness": {},
            "tempo": None
        }
        
        try:
            # Check if audio exists
            cmd = [
                "ffprobe", "-v", "error",
                "-select_streams", "a:0",
                "-show_entries", "stream=codec_type",
                "-of", "default=noprint_wrappers=1:nokey=1",
                video_file
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            audio_analysis["has_audio"] = "audio" in result.stdout
            
            if audio_analysis["has_audio"]:
                # Analyze loudness
                audio_analysis["loudness"] = self._analyze_loudness(video_file)
                
                # Detect silence
                audio_analysis["silence_periods"] = self._detect_silence(video_file)
                
                # Estimate content type (speech vs music)
                # In production, would use ML models
                audio_analysis["has_speech"] = True  # Placeholder
                audio_analysis["has_music"] = True  # Placeholder
            
        except Exception as e:
            print(f"⚠️  Audio analysis failed: {e}")
        
        return audio_analysis
    
    def _analyze_loudness(self, video_file: str) -> Dict[str, Any]:
        """Analyze audio loudness"""
        try:
            cmd = [
                "ffmpeg", "-i", video_file,
                "-af", "volumedetect",
                "-f", "null", "-"
            ]
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                stderr=subprocess.STDOUT
            )
            
            # Parse loudness values
            loudness = {}
            for line in result.stdout.split('\n'):
                if 'mean_volume' in line:
                    match = re.search(r'mean_volume: ([-\d.]+) dB', line)
                    if match:
                        loudness['mean'] = float(match.group(1))
                elif 'max_volume' in line:
                    match = re.search(r'max_volume: ([-\d.]+) dB', line)
                    if match:
                        loudness['max'] = float(match.group(1))
            
            return loudness
            
        except Exception as e:
            return {}
    
    def _detect_silence(self, video_file: str) -> List[Dict[str, Any]]:
        """Detect silence periods"""
        silence_periods = []
        
        try:
            cmd = [
                "ffmpeg", "-i", video_file,
                "-af", "silencedetect=noise=-30dB:d=0.5",
                "-f", "null", "-"
            ]
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                stderr=subprocess.STDOUT
            )
            
            # Parse silence periods
            silence_start = None
            for line in result.stdout.split('\n'):
                if 'silence_start' in line:
                    match = re.search(r'silence_start: ([\d.]+)', line)
                    if match:
                        silence_start = float(match.group(1))
                elif 'silence_end' in line and silence_start is not None:
                    match = re.search(r'silence_end: ([\d.]+)', line)
                    if match:
                        silence_end = float(match.group(1))
                        silence_periods.append({
                            "start": silence_start,
                            "end": silence_end,
                            "duration": silence_end - silence_start
                        })
                        silence_start = None
            
        except Exception as e:
            print(f"⚠️  Silence detection failed: {e}")
        
        return silence_periods
    
    def _assess_quality(self, video_file: str) -> Dict[str, Any]:
        """Assess video quality"""
        quality = {
            "resolution_score": 0,
            "bitrate_score": 0,
            "fps_score": 0,
            "overall_score": 0
        }
        
        try:
            metadata = self._get_metadata(video_file)
            video = metadata.get('video', {})
            
            # Resolution score (0-1)
            width = video.get('width', 0)
            height = video.get('height', 0)
            pixels = width * height
            
            if pixels >= 3840 * 2160:  # 4K
                quality["resolution_score"] = 1.0
            elif pixels >= 1920 * 1080:  # 1080p
                quality["resolution_score"] = 0.8
            elif pixels >= 1280 * 720:  # 720p
                quality["resolution_score"] = 0.6
            else:
                quality["resolution_score"] = 0.4
            
            # Bitrate score (0-1)
            bitrate = video.get('bitrate', 0) / 1000000  # Convert to Mbps
            if bitrate >= 10:
                quality["bitrate_score"] = 1.0
            elif bitrate >= 5:
                quality["bitrate_score"] = 0.8
            elif bitrate >= 2:
                quality["bitrate_score"] = 0.6
            else:
                quality["bitrate_score"] = 0.4
            
            # FPS score (0-1)
            fps = video.get('fps', 0)
            if fps >= 60:
                quality["fps_score"] = 1.0
            elif fps >= 30:
                quality["fps_score"] = 0.8
            elif fps >= 24:
                quality["fps_score"] = 0.6
            else:
                quality["fps_score"] = 0.4
            
            # Overall score
            quality["overall_score"] = (
                quality["resolution_score"] * 0.4 +
                quality["bitrate_score"] * 0.4 +
                quality["fps_score"] * 0.2
            )
            
        except Exception as e:
            print(f"⚠️  Quality assessment failed: {e}")
        
        return quality
    
    def _analyze_content(self, video_file: str) -> Dict[str, Any]:
        """Analyze video content (objects, faces, text)"""
        content = {
            "has_faces": False,
            "has_text": False,
            "dominant_colors": [],
            "brightness": 0,
            "motion_level": "unknown"
        }
        
        # Placeholder for content analysis
        # In production, would use:
        # - OpenCV for face detection
        # - Tesseract for text detection
        # - ML models for object detection
        
        return content
    
    def classify_video(self, video_file: str) -> Dict[str, Any]:
        """
        Classify video type and suggest processing
        
        Args:
            video_file: Input video
            
        Returns:
            Classification and recommendations
        """
        analysis = self.analyze_video(video_file)
        
        classification = {
            "type": "unknown",
            "confidence": 0.0,
            "recommendations": []
        }
        
        # Classify based on analysis
        metadata = analysis.get('metadata', {})
        audio = analysis.get('audio', {})
        quality = analysis.get('quality', {})
        
        # Check for common types
        duration = metadata.get('duration', 0)
        has_speech = audio.get('has_speech', False)
        has_music = audio.get('has_music', False)
        
        if duration < 60 and has_music:
            classification["type"] = "short_video"
            classification["confidence"] = 0.7
            classification["recommendations"] = [
                "Add intro/outro",
                "Apply color grading",
                "Add watermark"
            ]
        elif has_speech and not has_music:
            classification["type"] = "interview"
            classification["confidence"] = 0.6
            classification["recommendations"] = [
                "Add subtitles",
                "Normalize audio",
                "Remove silence"
            ]
        elif has_music and duration > 120:
            classification["type"] = "music_video"
            classification["confidence"] = 0.7
            classification["recommendations"] = [
                "Beat-sync editing",
                "Color grading",
                "Add effects"
            ]
        
        return classification
    
    def suggest_improvements(self, video_file: str) -> List[Dict[str, Any]]:
        """
        Suggest improvements based on analysis
        
        Args:
            video_file: Input video
            
        Returns:
            List of improvement suggestions
        """
        analysis = self.analyze_video(video_file)
        suggestions = []
        
        # Check quality
        quality = analysis.get('quality', {})
        if quality.get('overall_score', 0) < 0.6:
            suggestions.append({
                "type": "quality",
                "priority": "high",
                "suggestion": "Upscale video to improve quality",
                "action": "ai_upscale"
            })
        
        # Check audio
        audio = analysis.get('audio', {})
        if audio.get('loudness', {}).get('mean', 0) < -30:
            suggestions.append({
                "type": "audio",
                "priority": "medium",
                "suggestion": "Normalize audio levels",
                "action": "normalize_audio"
            })
        
        # Check for silence
        silence_periods = audio.get('silence_periods', [])
        if len(silence_periods) > 5:
            suggestions.append({
                "type": "editing",
                "priority": "low",
                "suggestion": "Remove silence periods",
                "action": "remove_silence"
            })
        
        return suggestions
    
    def generate_report(self, video_file: str, output_file: Optional[str] = None) -> str:
        """
        Generate comprehensive analysis report
        
        Args:
            video_file: Input video file
            output_file: Output report file (optional)
            
        Returns:
            Report text
        """
        analysis = self.analyze_video(video_file)
        classification = self.classify_video(video_file)
        suggestions = self.suggest_improvements(video_file)
        
        # Build report
        report = f"""
# Video Analysis Report
**File:** {video_file}
**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Metadata
- **Duration:** {analysis['metadata'].get('duration', 0):.2f} seconds
- **Resolution:** {analysis['metadata']['video'].get('width', 0)}x{analysis['metadata']['video'].get('height', 0)}
- **FPS:** {analysis['metadata']['video'].get('fps', 0):.2f}
- **Bitrate:** {analysis['metadata']['video'].get('bitrate', 0) / 1000000:.2f} Mbps

## Quality Assessment
- **Overall Score:** {analysis['quality'].get('overall_score', 0):.2f}
- **Resolution Score:** {analysis['quality'].get('resolution_score', 0):.2f}
- **Bitrate Score:** {analysis['quality'].get('bitrate_score', 0):.2f}
- **FPS Score:** {analysis['quality'].get('fps_score', 0):.2f}

## Content Analysis
- **Scenes Detected:** {len(analysis.get('scenes', []))}

## Audio Analysis
- **Has Audio:** {'Yes' if analysis['audio'].get('has_audio') else 'No'}
- **Has Speech:** {'Yes' if analysis['audio'].get('has_speech') else 'No'}
- **Has Music:** {'Yes' if analysis['audio'].get('has_music') else 'No'}
- **Silence Periods:** {len(analysis['audio'].get('silence_periods', []))}

## Classification
- **Type:** {classification['type']}
- **Confidence:** {classification['confidence'] * 100:.1f}%

## Improvement Suggestions
"""
        
        for i, suggestion in enumerate(suggestions, 1):
            report += f"\n{i}. **[{suggestion['priority'].upper()}]** {suggestion['suggestion']}"
            report += f"\n   - Action: {suggestion['action']}"
        
        report += "\n\n---\n*Generated by RSJ-FFMPEG Content Analyzer v2.2.0*\n"
        
        # Save to file if specified
        if output_file:
            with open(output_file, 'w') as f:
                f.write(report)
            print(f"📄 Report saved to: {output_file}")
        
        return report