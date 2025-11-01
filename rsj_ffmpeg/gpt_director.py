"""
RSJ-FFMPEG GPT Director
AI-Powered Video Editing with Natural Language Commands

Author: RAJSARASWATI JATAV
Version: 2.2.0
"""

import os
import json
import subprocess
from typing import Dict, Any, List, Optional, Tuple
from pathlib import Path
from datetime import datetime
import re


class GPTDirector:
    """
    GPT-powered video editing engine
    Enables natural language video editing commands
    """
    
    def __init__(self, config: Dict[str, Any], api_key: Optional[str] = None):
        """
        Initialize GPT Director
        
        Args:
            config: Configuration dictionary
            api_key: OpenAI API key (optional, can use env var)
        """
        self.config = config
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.editing_history = []
        self.templates = self._load_templates()
        
        # Check if OpenAI is available
        self.openai_available = False
        try:
            import openai
            if self.api_key:
                self.client = openai.OpenAI(api_key=self.api_key)
                self.openai_available = True
        except ImportError:
            print("⚠️  OpenAI not installed. Install with: pip install openai")
    
    def _load_templates(self) -> Dict[str, Any]:
        """Load editing templates"""
        return {
            "highlight_reel": {
                "description": "Create energetic highlight compilation",
                "transitions": ["fade", "wipe", "zoom"],
                "effects": ["speed_ramp", "color_boost"],
                "music_style": "upbeat"
            },
            "cinematic": {
                "description": "Cinematic storytelling edit",
                "transitions": ["fade", "dissolve"],
                "effects": ["color_grade", "slow_motion"],
                "music_style": "orchestral"
            },
            "vlog": {
                "description": "Casual vlog-style editing",
                "transitions": ["cut", "jump_cut"],
                "effects": ["text_overlay", "zoom"],
                "music_style": "background"
            },
            "commercial": {
                "description": "Professional commercial edit",
                "transitions": ["fade", "wipe"],
                "effects": ["color_grade", "text_overlay"],
                "music_style": "corporate"
            }
        }
    
    def edit_from_prompt(
        self,
        input_files: List[str],
        prompt: str,
        output: str,
        style: Optional[str] = None,
        duration: Optional[int] = None,
        music: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Edit video using natural language prompt
        
        Args:
            input_files: List of input video files
            prompt: Natural language editing instructions
            output: Output file path
            style: Editing style template (optional)
            duration: Target duration in seconds (optional)
            music: Background music file (optional)
            
        Returns:
            Editing result dictionary
        """
        print(f"🎬 GPT Director: Processing prompt...")
        print(f"📝 Prompt: {prompt}")
        
        # Parse prompt to extract editing instructions
        instructions = self._parse_prompt(prompt)
        
        # Apply style template if specified
        if style and style in self.templates:
            instructions.update(self.templates[style])
        
        # Build editing plan
        plan = self._create_editing_plan(
            input_files,
            instructions,
            duration,
            music
        )
        
        print(f"📋 Editing Plan:")
        for step in plan["steps"]:
            print(f"  • {step['action']}: {step['description']}")
        
        # Execute editing plan
        result = self._execute_plan(plan, output)
        
        # Log to history
        self.editing_history.append({
            "timestamp": datetime.now().isoformat(),
            "prompt": prompt,
            "plan": plan,
            "result": result
        })
        
        return result
    
    def _parse_prompt(self, prompt: str) -> Dict[str, Any]:
        """
        Parse natural language prompt into editing instructions
        Uses GPT if available, otherwise uses rule-based parsing
        """
        if self.openai_available:
            return self._parse_with_gpt(prompt)
        else:
            return self._parse_with_rules(prompt)
    
    def _parse_with_gpt(self, prompt: str) -> Dict[str, Any]:
        """Parse prompt using GPT API"""
        try:
            system_prompt = """You are a professional video editor. Parse the user's editing request 
            and extract key editing parameters. Return a JSON object with these fields:
            - style: editing style (cinematic, energetic, casual, etc.)
            - pace: editing pace (fast, medium, slow)
            - transitions: list of transition types
            - effects: list of effects to apply
            - focus: what to focus on (action, dialogue, scenery, etc.)
            - mood: desired mood (happy, dramatic, suspenseful, etc.)
            - music_style: type of background music
            """
            
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ],
                response_format={"type": "json_object"}
            )
            
            return json.loads(response.choices[0].message.content)
        except Exception as e:
            print(f"⚠️  GPT parsing failed: {e}")
            return self._parse_with_rules(prompt)
    
    def _parse_with_rules(self, prompt: str) -> Dict[str, Any]:
        """Parse prompt using rule-based approach"""
        prompt_lower = prompt.lower()
        
        instructions = {
            "style": "standard",
            "pace": "medium",
            "transitions": ["fade"],
            "effects": [],
            "focus": "general",
            "mood": "neutral",
            "music_style": "background"
        }
        
        # Detect style
        if any(word in prompt_lower for word in ["cinematic", "movie", "film"]):
            instructions["style"] = "cinematic"
        elif any(word in prompt_lower for word in ["energetic", "fast", "action"]):
            instructions["style"] = "energetic"
        elif any(word in prompt_lower for word in ["vlog", "casual", "personal"]):
            instructions["style"] = "vlog"
        
        # Detect pace
        if any(word in prompt_lower for word in ["fast", "quick", "rapid"]):
            instructions["pace"] = "fast"
        elif any(word in prompt_lower for word in ["slow", "calm", "relaxed"]):
            instructions["pace"] = "slow"
        
        # Detect transitions
        if "wipe" in prompt_lower:
            instructions["transitions"].append("wipe")
        if "zoom" in prompt_lower:
            instructions["transitions"].append("zoom")
        if "dissolve" in prompt_lower:
            instructions["transitions"].append("dissolve")
        
        # Detect effects
        if any(word in prompt_lower for word in ["color", "grade", "grading"]):
            instructions["effects"].append("color_grade")
        if any(word in prompt_lower for word in ["slow motion", "slowmo"]):
            instructions["effects"].append("slow_motion")
        if any(word in prompt_lower for word in ["text", "title", "caption"]):
            instructions["effects"].append("text_overlay")
        
        return instructions
    
    def _create_editing_plan(
        self,
        input_files: List[str],
        instructions: Dict[str, Any],
        duration: Optional[int],
        music: Optional[str]
    ) -> Dict[str, Any]:
        """Create detailed editing plan"""
        plan = {
            "input_files": input_files,
            "instructions": instructions,
            "target_duration": duration,
            "music": music,
            "steps": []
        }
        
        # Step 1: Analyze input files
        plan["steps"].append({
            "action": "analyze",
            "description": "Analyze input videos for content and quality"
        })
        
        # Step 2: Select best clips
        plan["steps"].append({
            "action": "select_clips",
            "description": f"Select clips based on {instructions.get('focus', 'general')} focus"
        })
        
        # Step 3: Apply effects
        if instructions.get("effects"):
            for effect in instructions["effects"]:
                plan["steps"].append({
                    "action": "apply_effect",
                    "description": f"Apply {effect} effect"
                })
        
        # Step 4: Add transitions
        plan["steps"].append({
            "action": "add_transitions",
            "description": f"Add {', '.join(instructions.get('transitions', ['fade']))} transitions"
        })
        
        # Step 5: Add music
        if music:
            plan["steps"].append({
                "action": "add_music",
                "description": "Add background music and sync to beats"
            })
        
        # Step 6: Final render
        plan["steps"].append({
            "action": "render",
            "description": "Render final video"
        })
        
        return plan
    
    def _execute_plan(self, plan: Dict[str, Any], output: str) -> Dict[str, Any]:
        """Execute the editing plan"""
        try:
            # For now, create a simple concatenation with effects
            # In production, this would execute each step individually
            
            input_files = plan["input_files"]
            instructions = plan["instructions"]
            
            # Create concat file
            concat_file = Path(output).parent / "concat_list.txt"
            with open(concat_file, 'w') as f:
                for file in input_files:
                    f.write(f"file '{file}'\n")
            
            # Build FFmpeg command
            cmd = [
                "ffmpeg", "-f", "concat", "-safe", "0",
                "-i", str(concat_file)
            ]
            
            # Add filters based on instructions
            filters = []
            
            # Apply pace adjustment
            pace = instructions.get("pace", "medium")
            if pace == "fast":
                filters.append("setpts=0.75*PTS")
            elif pace == "slow":
                filters.append("setpts=1.5*PTS")
            
            # Apply color grading if requested
            if "color_grade" in instructions.get("effects", []):
                filters.append("eq=contrast=1.1:brightness=0.05:saturation=1.2")
            
            # Add music if specified
            if plan.get("music"):
                cmd.extend(["-i", plan["music"]])
                cmd.extend(["-filter_complex", "[0:a][1:a]amix=inputs=2:duration=first"])
            
            # Apply video filters
            if filters:
                cmd.extend(["-vf", ",".join(filters)])
            
            # Output settings
            cmd.extend([
                "-c:v", "libx264",
                "-preset", "medium",
                "-crf", "23",
                "-c:a", "aac",
                "-b:a", "192k",
                "-y",
                output
            ])
            
            print(f"🎬 Executing: {' '.join(cmd)}")
            subprocess.run(cmd, check=True, capture_output=True)
            
            # Clean up
            concat_file.unlink()
            
            return {
                "status": "success",
                "output": output,
                "plan": plan,
                "message": "Video edited successfully using GPT Director"
            }
            
        except subprocess.CalledProcessError as e:
            return {
                "status": "failed",
                "error": str(e),
                "stderr": e.stderr.decode() if e.stderr else ""
            }
        except Exception as e:
            return {
                "status": "failed",
                "error": str(e)
            }
    
    def edit_from_script(
        self,
        script: str,
        footage_dir: str,
        output: str,
        auto_select: bool = True
    ) -> Dict[str, Any]:
        """
        Edit video based on a script file
        
        Args:
            script: Path to script file or script text
            footage_dir: Directory containing footage
            output: Output file path
            auto_select: Auto-select best clips for each scene
            
        Returns:
            Editing result
        """
        # Read script
        if os.path.exists(script):
            with open(script, 'r') as f:
                script_text = f.read()
        else:
            script_text = script
        
        # Parse script into scenes
        scenes = self._parse_script(script_text)
        
        # Match footage to scenes
        footage_files = list(Path(footage_dir).glob("*.mp4"))
        footage_files.extend(Path(footage_dir).glob("*.mov"))
        footage_files.extend(Path(footage_dir).glob("*.avi"))
        
        # Create editing plan for each scene
        scene_plans = []
        for scene in scenes:
            # Select best footage for this scene
            selected_clips = self._select_clips_for_scene(
                scene,
                footage_files,
                auto_select
            )
            
            scene_plans.append({
                "scene": scene,
                "clips": selected_clips
            })
        
        # Execute script-based editing
        return self._execute_script_edit(scene_plans, output)
    
    def _parse_script(self, script_text: str) -> List[Dict[str, Any]]:
        """Parse script into scenes"""
        scenes = []
        
        # Simple scene detection (look for scene headers)
        lines = script_text.split('\n')
        current_scene = None
        
        for line in lines:
            line = line.strip()
            
            # Detect scene headers (e.g., "SCENE 1:", "INT. OFFICE - DAY")
            if re.match(r'^(SCENE|INT\.|EXT\.)', line, re.IGNORECASE):
                if current_scene:
                    scenes.append(current_scene)
                
                current_scene = {
                    "header": line,
                    "description": "",
                    "dialogue": []
                }
            elif current_scene:
                # Check if it's dialogue (character name in caps)
                if line.isupper() and len(line.split()) <= 3:
                    current_scene["dialogue"].append({"character": line, "lines": []})
                elif current_scene["dialogue"]:
                    current_scene["dialogue"][-1]["lines"].append(line)
                else:
                    current_scene["description"] += line + " "
        
        if current_scene:
            scenes.append(current_scene)
        
        return scenes
    
    def _select_clips_for_scene(
        self,
        scene: Dict[str, Any],
        footage_files: List[Path],
        auto_select: bool
    ) -> List[str]:
        """Select best clips for a scene"""
        # In production, this would use AI to analyze footage
        # For now, return first available clips
        return [str(f) for f in footage_files[:3]]
    
    def _execute_script_edit(
        self,
        scene_plans: List[Dict[str, Any]],
        output: str
    ) -> Dict[str, Any]:
        """Execute script-based editing"""
        try:
            # Collect all clips
            all_clips = []
            for plan in scene_plans:
                all_clips.extend(plan["clips"])
            
            # Use edit_from_prompt with scene descriptions
            prompt = "Create a narrative video following the script scenes"
            
            return self.edit_from_prompt(
                input_files=all_clips,
                prompt=prompt,
                output=output,
                style="cinematic"
            )
            
        except Exception as e:
            return {
                "status": "failed",
                "error": str(e)
            }
    
    def analyze_content(
        self,
        video_file: str,
        analyze_audio: bool = True,
        detect_scenes: bool = True
    ) -> Dict[str, Any]:
        """
        Analyze video content for intelligent editing
        
        Args:
            video_file: Input video file
            analyze_audio: Analyze audio for beats/speech
            detect_scenes: Detect scene changes
            
        Returns:
            Analysis results
        """
        analysis = {
            "file": video_file,
            "duration": 0,
            "scenes": [],
            "audio_analysis": {},
            "metadata": {}
        }
        
        try:
            # Get video duration
            cmd = [
                "ffprobe", "-v", "error",
                "-show_entries", "format=duration",
                "-of", "default=noprint_wrappers=1:nokey=1",
                video_file
            ]
            result = subprocess.run(cmd, capture_output=True, text=True)
            analysis["duration"] = float(result.stdout.strip())
            
            # Detect scenes if requested
            if detect_scenes:
                analysis["scenes"] = self._detect_scenes(video_file)
            
            # Analyze audio if requested
            if analyze_audio:
                analysis["audio_analysis"] = self._analyze_audio(video_file)
            
            return analysis
            
        except Exception as e:
            return {
                "status": "failed",
                "error": str(e)
            }
    
    def _detect_scenes(self, video_file: str) -> List[Dict[str, Any]]:
        """Detect scene changes in video"""
        # Use FFmpeg scene detection
        scenes = []
        
        try:
            cmd = [
                "ffmpeg", "-i", video_file,
                "-vf", "select='gt(scene,0.3)',showinfo",
                "-f", "null", "-"
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, stderr=subprocess.STDOUT)
            
            # Parse scene timestamps from output
            for line in result.stdout.split('\n'):
                if 'pts_time' in line:
                    match = re.search(r'pts_time:([\d.]+)', line)
                    if match:
                        scenes.append({
                            "timestamp": float(match.group(1)),
                            "type": "scene_change"
                        })
            
        except Exception as e:
            print(f"⚠️  Scene detection failed: {e}")
        
        return scenes
    
    def _analyze_audio(self, video_file: str) -> Dict[str, Any]:
        """Analyze audio for beats and speech"""
        # Placeholder for audio analysis
        # In production, would use librosa or similar
        return {
            "has_speech": True,
            "has_music": True,
            "beats": [],
            "tempo": 120
        }
    
    def get_editing_history(self) -> List[Dict[str, Any]]:
        """Get editing history"""
        return self.editing_history
    
    def save_editing_plan(self, plan: Dict[str, Any], filepath: str):
        """Save editing plan to file"""
        with open(filepath, 'w') as f:
            json.dump(plan, f, indent=2)
    
    def load_editing_plan(self, filepath: str) -> Dict[str, Any]:
        """Load editing plan from file"""
        with open(filepath, 'r') as f:
            return json.load(f)