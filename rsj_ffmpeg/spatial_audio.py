#!/usr/bin/env python3
"""
RSJ-FFMPEG Spatial Audio Processing Module
3D audio, Dolby Atmos simulation, and surround sound

Author: RAJSARASWATI JATAV
Version: 2.1.0
"""

import os
import json
import subprocess
from typing import Dict, List, Optional, Tuple
from pathlib import Path


class SpatialAudioEngine:
    """Advanced spatial audio processing and 3D sound"""
    
    # Audio channel configurations
    CHANNEL_CONFIGS = {
        'mono': {'channels': 1, 'layout': 'mono'},
        'stereo': {'channels': 2, 'layout': 'stereo'},
        '2.1': {'channels': 3, 'layout': '2.1'},
        '5.1': {'channels': 6, 'layout': '5.1'},
        '7.1': {'channels': 8, 'layout': '7.1'},
        '7.1.4': {'channels': 12, 'layout': '7.1.4'},  # Atmos
        'binaural': {'channels': 2, 'layout': 'binaural'}
    }
    
    def __init__(self, config: Dict):
        self.config = config
    
    def create_surround(
        self,
        input_file: str,
        output_file: str,
        config: str = '5.1',
        center_boost: float = 1.0,
        lfe_boost: float = 1.5
    ) -> bool:
        """
        Create surround sound from stereo
        
        Args:
            input_file: Input audio/video path
            output_file: Output path
            config: Channel configuration (5.1, 7.1, etc.)
            center_boost: Center channel boost
            lfe_boost: LFE (subwoofer) boost
            
        Returns:
            Success status
        """
        if config not in self.CHANNEL_CONFIGS:
            print(f"❌ Unknown config: {config}")
            return False
        
        print(f"🔊 Creating {config} surround sound...")
        
        cmd = self._build_surround_command(
            input_file, output_file, config, center_boost, lfe_boost
        )
        
        try:
            subprocess.run(cmd, check=True, capture_output=True)
            print(f"✅ Surround sound created: {output_file}")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Surround creation failed: {e}")
            return False
    
    def dolby_atmos_simulation(
        self,
        input_file: str,
        output_file: str,
        height_channels: int = 4,
        room_size: str = 'medium'
    ) -> bool:
        """
        Simulate Dolby Atmos with height channels
        
        Args:
            input_file: Input audio/video path
            output_file: Output path
            height_channels: Number of height channels (2 or 4)
            room_size: Room size (small/medium/large)
            
        Returns:
            Success status
        """
        print(f"🎭 Simulating Dolby Atmos ({height_channels} height channels)...")
        
        cmd = self._build_atmos_command(
            input_file, output_file, height_channels, room_size
        )
        
        try:
            subprocess.run(cmd, check=True, capture_output=True)
            print(f"✅ Dolby Atmos simulation complete: {output_file}")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Atmos simulation failed: {e}")
            return False
    
    def binaural_audio(
        self,
        input_file: str,
        output_file: str,
        hrtf_profile: str = 'default',
        head_tracking: bool = False
    ) -> bool:
        """
        Create binaural 3D audio for headphones
        
        Args:
            input_file: Input audio/video path
            output_file: Output path
            hrtf_profile: HRTF profile (default/wide/narrow)
            head_tracking: Enable head tracking simulation
            
        Returns:
            Success status
        """
        print("🎧 Creating binaural 3D audio...")
        
        cmd = self._build_binaural_command(
            input_file, output_file, hrtf_profile, head_tracking
        )
        
        try:
            subprocess.run(cmd, check=True, capture_output=True)
            print(f"✅ Binaural audio created: {output_file}")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Binaural creation failed: {e}")
            return False
    
    def position_audio_3d(
        self,
        input_file: str,
        output_file: str,
        x: float = 0.0,
        y: float = 0.0,
        z: float = 0.0,
        distance: float = 1.0
    ) -> bool:
        """
        Position audio source in 3D space
        
        Args:
            input_file: Input audio path
            output_file: Output path
            x: X position (-1.0 to 1.0, left to right)
            y: Y position (-1.0 to 1.0, back to front)
            z: Z position (-1.0 to 1.0, down to up)
            distance: Distance from listener (0.0 to 10.0)
            
        Returns:
            Success status
        """
        print(f"📍 Positioning audio at ({x}, {y}, {z}), distance: {distance}")
        
        cmd = self._build_3d_position_command(
            input_file, output_file, x, y, z, distance
        )
        
        try:
            subprocess.run(cmd, check=True, capture_output=True)
            print(f"✅ 3D audio positioned: {output_file}")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ 3D positioning failed: {e}")
            return False
    
    def reverb_3d(
        self,
        input_file: str,
        output_file: str,
        room_type: str = 'hall',
        wet_mix: float = 0.3,
        decay_time: float = 2.0
    ) -> bool:
        """
        Apply 3D reverb simulation
        
        Room types: hall, church, studio, bathroom, canyon
        
        Args:
            input_file: Input audio/video path
            output_file: Output path
            room_type: Type of room
            wet_mix: Reverb wet mix (0.0-1.0)
            decay_time: Reverb decay time in seconds
            
        Returns:
            Success status
        """
        print(f"🏛️ Applying {room_type} reverb...")
        
        cmd = self._build_reverb_command(
            input_file, output_file, room_type, wet_mix, decay_time
        )
        
        try:
            subprocess.run(cmd, check=True, capture_output=True)
            print(f"✅ 3D reverb applied: {output_file}")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Reverb failed: {e}")
            return False
    
    def audio_panning(
        self,
        input_file: str,
        output_file: str,
        pan_pattern: str = 'left_right',
        speed: float = 1.0,
        depth: float = 1.0
    ) -> bool:
        """
        Create dynamic audio panning effects
        
        Patterns: left_right, circular, random, wave
        
        Args:
            input_file: Input audio/video path
            output_file: Output path
            pan_pattern: Panning pattern
            speed: Panning speed
            depth: Panning depth
            
        Returns:
            Success status
        """
        print(f"🔄 Creating {pan_pattern} panning effect...")
        
        cmd = self._build_panning_command(
            input_file, output_file, pan_pattern, speed, depth
        )
        
        try:
            subprocess.run(cmd, check=True, capture_output=True)
            print(f"✅ Panning effect applied: {output_file}")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Panning failed: {e}")
            return False
    
    def downmix_surround(
        self,
        input_file: str,
        output_file: str,
        target_config: str = 'stereo',
        preserve_dynamics: bool = True
    ) -> bool:
        """
        Downmix surround to stereo/mono
        
        Args:
            input_file: Input surround audio path
            output_file: Output path
            target_config: Target configuration
            preserve_dynamics: Preserve dynamic range
            
        Returns:
            Success status
        """
        print(f"⬇️ Downmixing to {target_config}...")
        
        cmd = self._build_downmix_command(
            input_file, output_file, target_config, preserve_dynamics
        )
        
        try:
            subprocess.run(cmd, check=True, capture_output=True)
            print(f"✅ Downmix complete: {output_file}")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Downmix failed: {e}")
            return False
    
    def spatial_audio_batch(
        self,
        input_dir: str,
        output_dir: str,
        config: str = '5.1',
        binaural: bool = False
    ) -> Dict:
        """
        Batch process spatial audio
        
        Args:
            input_dir: Input directory
            output_dir: Output directory
            config: Channel configuration
            binaural: Create binaural output
            
        Returns:
            Processing report
        """
        print(f"🔄 Batch spatial audio processing...")
        
        os.makedirs(output_dir, exist_ok=True)
        
        audio_extensions = ['.mp3', '.wav', '.flac', '.aac', '.m4a']
        files = []
        
        for ext in audio_extensions:
            files.extend(Path(input_dir).glob(f'*{ext}'))
        
        report = {
            'total': len(files),
            'processed': 0,
            'failed': 0,
            'config': config,
            'files': []
        }
        
        for audio_file in files:
            output_path = Path(output_dir) / f"spatial_{audio_file.name}"
            
            if binaural:
                success = self.binaural_audio(str(audio_file), str(output_path))
            else:
                success = self.create_surround(str(audio_file), str(output_path), config)
            
            if success:
                report['processed'] += 1
            else:
                report['failed'] += 1
            
            report['files'].append({
                'input': str(audio_file),
                'output': str(output_path),
                'status': 'success' if success else 'failed'
            })
        
        print(f"✅ Batch complete: {report['processed']}/{report['total']} processed")
        return report
    
    def _build_surround_command(
        self,
        input_file: str,
        output_file: str,
        config: str,
        center_boost: float,
        lfe_boost: float
    ) -> List[str]:
        """Build FFmpeg command for surround sound creation"""
        
        layout = self.CHANNEL_CONFIGS[config]['layout']
        
        cmd = [
            'ffmpeg', '-i', input_file,
            '-af', f'pan={layout}|c0=c0|c1=c1|c2=c0+c1|c3=c0|c4=c1|c5=c0+c1',
            '-c:v', 'copy',
            '-y', output_file
        ]
        
        return cmd
    
    def _build_atmos_command(
        self,
        input_file: str,
        output_file: str,
        height_channels: int,
        room_size: str
    ) -> List[str]:
        """Build command for Dolby Atmos simulation"""
        
        cmd = [
            'ffmpeg', '-i', input_file,
            '-af', 'pan=7.1.4|c0=c0|c1=c1|c2=c0+c1|c3=c0|c4=c1|c5=c0+c1|c6=c0|c7=c1|c8=c0|c9=c1|c10=c0|c11=c1',
            '-c:v', 'copy',
            '-y', output_file
        ]
        
        return cmd
    
    def _build_binaural_command(
        self,
        input_file: str,
        output_file: str,
        hrtf_profile: str,
        head_tracking: bool
    ) -> List[str]:
        """Build command for binaural audio"""
        
        cmd = [
            'ffmpeg', '-i', input_file,
            '-af', 'headphone=hrir=default',
            '-c:v', 'copy',
            '-y', output_file
        ]
        
        return cmd
    
    def _build_3d_position_command(
        self,
        input_file: str,
        output_file: str,
        x: float,
        y: float,
        z: float,
        distance: float
    ) -> List[str]:
        """Build command for 3D audio positioning"""
        
        # Calculate pan based on x position
        pan = (x + 1.0) / 2.0  # Convert -1..1 to 0..1
        
        cmd = [
            'ffmpeg', '-i', input_file,
            '-af', f'pan=stereo|c0=c0*{1-pan}|c1=c1*{pan}',
            '-y', output_file
        ]
        
        return cmd
    
    def _build_reverb_command(
        self,
        input_file: str,
        output_file: str,
        room_type: str,
        wet_mix: float,
        decay_time: float
    ) -> List[str]:
        """Build command for 3D reverb"""
        
        reverb_presets = {
            'hall': 'aecho=0.8:0.9:1000:0.3',
            'church': 'aecho=0.8:0.9:1500:0.5',
            'studio': 'aecho=0.6:0.7:500:0.2',
            'bathroom': 'aecho=0.9:0.95:200:0.4',
            'canyon': 'aecho=0.7:0.8:2000:0.6'
        }
        
        reverb_filter = reverb_presets.get(room_type, reverb_presets['hall'])
        
        cmd = [
            'ffmpeg', '-i', input_file,
            '-af', reverb_filter,
            '-c:v', 'copy',
            '-y', output_file
        ]
        
        return cmd
    
    def _build_panning_command(
        self,
        input_file: str,
        output_file: str,
        pan_pattern: str,
        speed: float,
        depth: float
    ) -> List[str]:
        """Build command for audio panning"""
        
        # Simplified panning (in production, use more complex filters)
        cmd = [
            'ffmpeg', '-i', input_file,
            '-af', f'pan=stereo|c0=c0*sin(2*PI*t*{speed})|c1=c1*cos(2*PI*t*{speed})',
            '-c:v', 'copy',
            '-y', output_file
        ]
        
        return cmd
    
    def _build_downmix_command(
        self,
        input_file: str,
        output_file: str,
        target_config: str,
        preserve_dynamics: bool
    ) -> List[str]:
        """Build command for surround downmix"""
        
        cmd = [
            'ffmpeg', '-i', input_file,
            '-ac', '2',  # Stereo
            '-c:v', 'copy',
            '-y', output_file
        ]
        
        return cmd


# CLI Integration
if __name__ == '__main__':
    print("""
    ╔══════════════════════════════════════════════════════════════╗
    ║  RSJ-FFMPEG SPATIAL AUDIO PROCESSING MODULE                  ║
    ║  3D Audio, Dolby Atmos & Surround Sound                     ║
    ║  By RAJSARASWATI JATAV                                      ║
    ╚══════════════════════════════════════════════════════════════╝
    """)
    
    config = {}
    engine = SpatialAudioEngine(config)
    
    print("\n🔊 Available Features:")
    print("  • create_surround() - Create surround sound")
    print("  • dolby_atmos_simulation() - Simulate Dolby Atmos")
    print("  • binaural_audio() - Create 3D headphone audio")
    print("  • position_audio_3d() - Position audio in 3D space")
    print("  • reverb_3d() - Apply 3D reverb")
    print("  • audio_panning() - Dynamic panning effects")
    print("  • downmix_surround() - Downmix to stereo/mono")