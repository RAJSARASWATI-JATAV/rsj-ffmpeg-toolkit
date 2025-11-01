#!/usr/bin/env python3
"""
RSJ-FFMPEG Advanced Color Grading Module
Professional color grading presets and LUT management

Author: RAJSARASWATI JATAV
Version: 2.1.0
"""

import os
import json
import subprocess
from typing import Dict, List, Optional, Tuple
from pathlib import Path


class ColorGradingEngine:
    """Advanced color grading with professional presets"""
    
    # Professional LUT Presets Library
    PRESETS = {
        'cinematic': {
            'name': 'Cinematic',
            'description': 'Hollywood blockbuster look',
            'curves': {'shadows': -10, 'midtones': 5, 'highlights': 10},
            'saturation': 1.2,
            'contrast': 1.15
        },
        'cyberpunk': {
            'name': 'Cyberpunk',
            'description': 'Neon-soaked futuristic aesthetic',
            'curves': {'shadows': -20, 'midtones': 0, 'highlights': 15},
            'saturation': 1.5,
            'tint': {'cyan': 10, 'magenta': 5}
        },
        'vintage': {
            'name': 'Vintage Film',
            'description': 'Classic film emulation',
            'curves': {'shadows': 5, 'midtones': -5, 'highlights': 0},
            'saturation': 0.8,
            'grain': 15
        },
        'moody': {
            'name': 'Moody Dark',
            'description': 'Dark and atmospheric',
            'curves': {'shadows': -30, 'midtones': -10, 'highlights': 5},
            'saturation': 0.9,
            'contrast': 1.3
        },
        'vibrant': {
            'name': 'Vibrant Pop',
            'description': 'Bright and colorful',
            'curves': {'shadows': 0, 'midtones': 10, 'highlights': 15},
            'saturation': 1.6,
            'contrast': 1.1
        },
        'noir': {
            'name': 'Film Noir',
            'description': 'Classic black and white',
            'curves': {'shadows': -15, 'midtones': 0, 'highlights': 10},
            'saturation': 0.0,
            'contrast': 1.4
        },
        'sunset': {
            'name': 'Golden Sunset',
            'description': 'Warm golden hour',
            'curves': {'shadows': 0, 'midtones': 5, 'highlights': 10},
            'temperature': 20,
            'saturation': 1.3
        },
        'arctic': {
            'name': 'Arctic Blue',
            'description': 'Cool blue tones',
            'curves': {'shadows': -5, 'midtones': 0, 'highlights': 5},
            'temperature': -20,
            'saturation': 1.1
        },
        'sepia': {
            'name': 'Sepia Tone',
            'description': 'Classic sepia photograph',
            'curves': {'shadows': 0, 'midtones': 5, 'highlights': 10},
            'tint': {'red': 20, 'green': 10, 'blue': 0},
            'saturation': 0.7
        },
        'teal_orange': {
            'name': 'Teal & Orange',
            'description': 'Modern blockbuster look',
            'curves': {'shadows': -10, 'midtones': 0, 'highlights': 10},
            'tint': {'cyan': 15, 'orange': 15},
            'saturation': 1.25
        },
        'bleach_bypass': {
            'name': 'Bleach Bypass',
            'description': 'Desaturated high contrast',
            'curves': {'shadows': -20, 'midtones': 0, 'highlights': 20},
            'saturation': 0.5,
            'contrast': 1.5
        },
        'dream': {
            'name': 'Dreamy Soft',
            'description': 'Soft ethereal look',
            'curves': {'shadows': 10, 'midtones': 5, 'highlights': 0},
            'saturation': 0.9,
            'blur': 2
        },
        'horror': {
            'name': 'Horror Dark',
            'description': 'Creepy horror aesthetic',
            'curves': {'shadows': -40, 'midtones': -20, 'highlights': 0},
            'saturation': 0.6,
            'contrast': 1.6,
            'tint': {'green': 10}
        },
        'anime': {
            'name': 'Anime Style',
            'description': 'Vibrant anime colors',
            'curves': {'shadows': 0, 'midtones': 15, 'highlights': 20},
            'saturation': 1.8,
            'contrast': 1.2
        },
        'documentary': {
            'name': 'Documentary',
            'description': 'Natural realistic look',
            'curves': {'shadows': 0, 'midtones': 0, 'highlights': 0},
            'saturation': 1.0,
            'contrast': 1.05
        },
        'music_video': {
            'name': 'Music Video',
            'description': 'High energy colorful',
            'curves': {'shadows': -10, 'midtones': 10, 'highlights': 15},
            'saturation': 1.7,
            'contrast': 1.3
        },
        'instagram': {
            'name': 'Instagram',
            'description': 'Social media optimized',
            'curves': {'shadows': 5, 'midtones': 10, 'highlights': 10},
            'saturation': 1.4,
            'contrast': 1.15
        },
        'vlog': {
            'name': 'Vlog Style',
            'description': 'Clean vlog aesthetic',
            'curves': {'shadows': 0, 'midtones': 5, 'highlights': 10},
            'saturation': 1.2,
            'contrast': 1.1
        },
        'commercial': {
            'name': 'Commercial',
            'description': 'Professional commercial',
            'curves': {'shadows': -5, 'midtones': 5, 'highlights': 15},
            'saturation': 1.3,
            'contrast': 1.2
        },
        'rsj_signature': {
            'name': 'RSJ Signature',
            'description': 'RAJSARASWATI JATAV signature look',
            'curves': {'shadows': -15, 'midtones': 5, 'highlights': 15},
            'saturation': 1.4,
            'contrast': 1.25,
            'tint': {'cyan': 8, 'magenta': 3}
        }
    }
    
    def __init__(self, config: Dict):
        self.config = config
        self.custom_luts_dir = config.get('custom_luts_dir', './luts/')
        os.makedirs(self.custom_luts_dir, exist_ok=True)
    
    def apply_preset(
        self,
        input_file: str,
        output_file: str,
        preset: str,
        intensity: float = 1.0
    ) -> bool:
        """
        Apply professional color grading preset
        
        Args:
            input_file: Input video path
            output_file: Output video path
            preset: Preset name from PRESETS
            intensity: Effect intensity (0.0-1.0)
            
        Returns:
            Success status
        """
        if preset not in self.PRESETS:
            print(f"❌ Unknown preset: {preset}")
            print(f"Available presets: {', '.join(self.PRESETS.keys())}")
            return False
        
        preset_config = self.PRESETS[preset]
        print(f"🎨 Applying '{preset_config['name']}' preset...")
        
        cmd = self._build_preset_command(
            input_file, output_file, preset_config, intensity
        )
        
        try:
            subprocess.run(cmd, check=True, capture_output=True)
            print(f"✅ Color grading complete: {output_file}")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Color grading failed: {e}")
            return False
    
    def apply_lut(
        self,
        input_file: str,
        output_file: str,
        lut_file: str,
        intensity: float = 1.0
    ) -> bool:
        """
        Apply custom LUT file
        
        Args:
            input_file: Input video path
            output_file: Output video path
            lut_file: LUT file path (.cube, .3dl)
            intensity: LUT intensity (0.0-1.0)
            
        Returns:
            Success status
        """
        if not os.path.exists(lut_file):
            print(f"❌ LUT file not found: {lut_file}")
            return False
        
        print(f"🎨 Applying LUT: {lut_file}")
        
        cmd = [
            'ffmpeg', '-i', input_file,
            '-vf', f'lut3d={lut_file}:interp=trilinear',
            '-c:a', 'copy',
            '-y', output_file
        ]
        
        try:
            subprocess.run(cmd, check=True, capture_output=True)
            print(f"✅ LUT applied: {output_file}")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ LUT application failed: {e}")
            return False
    
    def create_custom_lut(
        self,
        name: str,
        curves: Dict,
        saturation: float = 1.0,
        contrast: float = 1.0,
        temperature: int = 0,
        tint: Optional[Dict] = None
    ) -> str:
        """
        Create custom LUT file
        
        Args:
            name: LUT name
            curves: Shadow/midtone/highlight adjustments
            saturation: Saturation multiplier
            contrast: Contrast multiplier
            temperature: Color temperature shift
            tint: Color tint adjustments
            
        Returns:
            Path to created LUT file
        """
        lut_path = os.path.join(self.custom_luts_dir, f'{name}.cube')
        
        print(f"🎨 Creating custom LUT: {name}")
        
        # Generate LUT data (simplified - in production use proper LUT generation)
        lut_data = self._generate_lut_data(
            curves, saturation, contrast, temperature, tint
        )
        
        with open(lut_path, 'w') as f:
            f.write(lut_data)
        
        print(f"✅ LUT created: {lut_path}")
        return lut_path
    
    def batch_grade(
        self,
        input_dir: str,
        output_dir: str,
        preset: str,
        intensity: float = 1.0
    ) -> Dict:
        """
        Batch color grade directory
        
        Args:
            input_dir: Input directory
            output_dir: Output directory
            preset: Preset to apply
            intensity: Effect intensity
            
        Returns:
            Processing report
        """
        print(f"🔄 Batch color grading with '{preset}' preset...")
        
        os.makedirs(output_dir, exist_ok=True)
        
        video_extensions = ['.mp4', '.avi', '.mov', '.mkv', '.webm']
        files = []
        
        for ext in video_extensions:
            files.extend(Path(input_dir).glob(f'*{ext}'))
        
        report = {
            'total': len(files),
            'processed': 0,
            'failed': 0,
            'preset': preset,
            'files': []
        }
        
        for video_file in files:
            output_path = Path(output_dir) / f"graded_{video_file.name}"
            
            success = self.apply_preset(
                str(video_file),
                str(output_path),
                preset,
                intensity
            )
            
            if success:
                report['processed'] += 1
            else:
                report['failed'] += 1
            
            report['files'].append({
                'input': str(video_file),
                'output': str(output_path),
                'status': 'success' if success else 'failed'
            })
        
        print(f"✅ Batch complete: {report['processed']}/{report['total']} processed")
        return report
    
    def compare_presets(
        self,
        input_file: str,
        output_dir: str,
        presets: Optional[List[str]] = None
    ) -> List[str]:
        """
        Generate comparison of multiple presets
        
        Args:
            input_file: Input video path
            output_dir: Output directory
            presets: List of presets (None = all)
            
        Returns:
            List of generated comparison files
        """
        os.makedirs(output_dir, exist_ok=True)
        
        if presets is None:
            presets = list(self.PRESETS.keys())
        
        print(f"🎨 Generating {len(presets)} preset comparisons...")
        
        output_files = []
        
        for preset in presets:
            output_path = os.path.join(output_dir, f"{preset}_comparison.mp4")
            
            if self.apply_preset(input_file, output_path, preset):
                output_files.append(output_path)
        
        print(f"✅ Generated {len(output_files)} comparison files")
        return output_files
    
    def list_presets(self) -> None:
        """Display all available presets"""
        print("\n🎨 Available Color Grading Presets:\n")
        
        for key, preset in self.PRESETS.items():
            print(f"  • {preset['name']} ({key})")
            print(f"    {preset['description']}")
            print()
    
    def _build_preset_command(
        self,
        input_file: str,
        output_file: str,
        preset_config: Dict,
        intensity: float
    ) -> List[str]:
        """Build FFmpeg command for preset application"""
        
        filters = []
        
        # Curves adjustment
        if 'curves' in preset_config:
            curves = preset_config['curves']
            filters.append(f"curves=all='{curves.get('shadows', 0)}/{curves.get('midtones', 0)}/{curves.get('highlights', 0)}'")
        
        # Saturation
        if 'saturation' in preset_config:
            sat = preset_config['saturation'] * intensity
            filters.append(f'eq=saturation={sat}')
        
        # Contrast
        if 'contrast' in preset_config:
            cont = preset_config['contrast'] * intensity
            filters.append(f'eq=contrast={cont}')
        
        # Temperature (simplified)
        if 'temperature' in preset_config:
            temp = preset_config['temperature'] * intensity
            if temp > 0:
                filters.append(f'colortemperature={5500 + temp * 10}')
            else:
                filters.append(f'colortemperature={5500 + temp * 10}')
        
        filter_str = ','.join(filters) if filters else 'null'
        
        cmd = [
            'ffmpeg', '-i', input_file,
            '-vf', filter_str,
            '-c:a', 'copy',
            '-y', output_file
        ]
        
        return cmd
    
    def _generate_lut_data(
        self,
        curves: Dict,
        saturation: float,
        contrast: float,
        temperature: int,
        tint: Optional[Dict]
    ) -> str:
        """Generate LUT file data (simplified)"""
        
        # Basic .cube LUT format
        lut_data = f"""# RSJ-FFMPEG Custom LUT
# Generated by RAJSARASWATI JATAV
TITLE "Custom LUT"
LUT_3D_SIZE 33

# LUT Data (simplified)
0.0 0.0 0.0
1.0 1.0 1.0
"""
        return lut_data


# CLI Integration
if __name__ == '__main__':
    print("""
    ╔══════════════════════════════════════════════════════════════╗
    ║  RSJ-FFMPEG ADVANCED COLOR GRADING MODULE                    ║
    ║  Professional Color Grading & LUT Management                 ║
    ║  By RAJSARASWATI JATAV                                      ║
    ╚══════════════════════════════════════════════════════════════╝
    """)
    
    config = {}
    engine = ColorGradingEngine(config)
    
    # List all presets
    engine.list_presets()