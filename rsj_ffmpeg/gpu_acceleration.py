#!/usr/bin/env python3
"""
RSJ-FFMPEG GPU Acceleration Module
Hardware encoding/decoding with NVIDIA CUDA, AMD ROCm, Intel QSV

Author: RAJSARASWATI JATAV
Version: 2.1.0
"""

import os
import subprocess
import platform
from typing import Dict, List, Optional, Tuple


class GPUAccelerationEngine:
    """GPU-accelerated video processing"""
    
    # Hardware encoder mappings
    ENCODERS = {
        'nvidia': {
            'h264': 'h264_nvenc',
            'h265': 'hevc_nvenc',
            'av1': 'av1_nvenc'
        },
        'amd': {
            'h264': 'h264_amf',
            'h265': 'hevc_amf'
        },
        'intel': {
            'h264': 'h264_qsv',
            'h265': 'hevc_qsv',
            'av1': 'av1_qsv'
        },
        'apple': {
            'h264': 'h264_videotoolbox',
            'h265': 'hevc_videotoolbox'
        }
    }
    
    # Hardware decoder mappings
    DECODERS = {
        'nvidia': {
            'h264': 'h264_cuvid',
            'h265': 'hevc_cuvid',
            'av1': 'av1_cuvid'
        },
        'amd': {
            'h264': 'h264',
            'h265': 'hevc'
        },
        'intel': {
            'h264': 'h264_qsv',
            'h265': 'hevc_qsv'
        }
    }
    
    def __init__(self, config: Dict):
        self.config = config
        self.gpu_vendor = self.detect_gpu()
        self.cuda_available = self.check_cuda()
    
    def detect_gpu(self) -> str:
        """
        Detect available GPU hardware
        
        Returns:
            GPU vendor (nvidia/amd/intel/apple/none)
        """
        print("🔍 Detecting GPU hardware...")
        
        # Check for NVIDIA
        try:
            result = subprocess.run(
                ['nvidia-smi'], 
                capture_output=True, 
                text=True, 
                timeout=5
            )
            if result.returncode == 0:
                print("✅ NVIDIA GPU detected")
                return 'nvidia'
        except:
            pass
        
        # Check for AMD
        try:
            result = subprocess.run(
                ['rocm-smi'], 
                capture_output=True, 
                text=True, 
                timeout=5
            )
            if result.returncode == 0:
                print("✅ AMD GPU detected")
                return 'amd'
        except:
            pass
        
        # Check for Intel
        if platform.system() == 'Windows':
            # Intel QSV check
            print("ℹ️ Intel GPU may be available")
            return 'intel'
        
        # Check for Apple Silicon
        if platform.system() == 'Darwin' and platform.machine() == 'arm64':
            print("✅ Apple Silicon detected")
            return 'apple'
        
        print("⚠️ No GPU detected, using CPU")
        return 'none'
    
    def check_cuda(self) -> bool:
        """Check if CUDA is available"""
        if self.gpu_vendor != 'nvidia':
            return False
        
        try:
            result = subprocess.run(
                ['nvcc', '--version'],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                print("✅ CUDA toolkit available")
                return True
        except:
            pass
        
        print("⚠️ CUDA toolkit not found")
        return False
    
    def encode_gpu(
        self,
        input_file: str,
        output_file: str,
        codec: str = 'h264',
        preset: str = 'medium',
        quality: int = 23
    ) -> bool:
        """
        Encode video using GPU acceleration
        
        Args:
            input_file: Input video path
            output_file: Output video path
            codec: Video codec (h264/h265/av1)
            preset: Encoding preset (fast/medium/slow)
            quality: Quality (0-51, lower is better)
            
        Returns:
            Success status
        """
        if self.gpu_vendor == 'none':
            print("⚠️ No GPU available, falling back to CPU encoding")
            return self._encode_cpu(input_file, output_file, codec, quality)
        
        encoder = self.ENCODERS.get(self.gpu_vendor, {}).get(codec)
        
        if not encoder:
            print(f"⚠️ {codec} not supported on {self.gpu_vendor}, using CPU")
            return self._encode_cpu(input_file, output_file, codec, quality)
        
        print(f"🚀 GPU encoding with {encoder}...")
        
        cmd = self._build_gpu_encode_command(
            input_file, output_file, encoder, preset, quality
        )
        
        try:
            subprocess.run(cmd, check=True, capture_output=True)
            print(f"✅ GPU encoding complete: {output_file}")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ GPU encoding failed: {e}")
            return False
    
    def decode_gpu(
        self,
        input_file: str,
        output_file: str,
        codec: str = 'h264'
    ) -> bool:
        """
        Decode video using GPU acceleration
        
        Args:
            input_file: Input video path
            output_file: Output video path
            codec: Video codec
            
        Returns:
            Success status
        """
        if self.gpu_vendor == 'none':
            print("⚠️ No GPU available for decoding")
            return False
        
        decoder = self.DECODERS.get(self.gpu_vendor, {}).get(codec)
        
        if not decoder:
            print(f"⚠️ {codec} decoder not available")
            return False
        
        print(f"🚀 GPU decoding with {decoder}...")
        
        cmd = [
            'ffmpeg',
            '-hwaccel', 'auto',
            '-c:v', decoder,
            '-i', input_file,
            '-c:v', 'copy',
            '-c:a', 'copy',
            '-y', output_file
        ]
        
        try:
            subprocess.run(cmd, check=True, capture_output=True)
            print(f"✅ GPU decoding complete: {output_file}")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ GPU decoding failed: {e}")
            return False
    
    def benchmark_gpu(self, test_file: Optional[str] = None) -> Dict:
        """
        Benchmark GPU encoding performance
        
        Args:
            test_file: Optional test video file
            
        Returns:
            Benchmark results
        """
        print("📊 Running GPU benchmark...")
        
        if not test_file:
            # Create test file
            test_file = self._create_test_video()
        
        results = {
            'gpu_vendor': self.gpu_vendor,
            'cuda_available': self.cuda_available,
            'encoders': {},
            'cpu_baseline': 0
        }
        
        # Test CPU encoding
        print("Testing CPU encoding...")
        cpu_time = self._benchmark_encode(test_file, 'cpu', 'h264')
        results['cpu_baseline'] = cpu_time
        
        # Test GPU encoders
        if self.gpu_vendor != 'none':
            for codec in ['h264', 'h265']:
                encoder = self.ENCODERS.get(self.gpu_vendor, {}).get(codec)
                if encoder:
                    print(f"Testing {encoder}...")
                    gpu_time = self._benchmark_encode(test_file, 'gpu', codec)
                    speedup = cpu_time / gpu_time if gpu_time > 0 else 0
                    
                    results['encoders'][codec] = {
                        'time': gpu_time,
                        'speedup': f"{speedup:.2f}x"
                    }
        
        print("\n📊 Benchmark Results:")
        print(f"  GPU: {self.gpu_vendor}")
        print(f"  CPU Baseline: {cpu_time:.2f}s")
        for codec, data in results['encoders'].items():
            print(f"  {codec.upper()}: {data['time']:.2f}s ({data['speedup']} faster)")
        
        return results
    
    def get_gpu_info(self) -> Dict:
        """
        Get detailed GPU information
        
        Returns:
            GPU information dictionary
        """
        info = {
            'vendor': self.gpu_vendor,
            'cuda_available': self.cuda_available,
            'supported_codecs': [],
            'memory': 'Unknown'
        }
        
        if self.gpu_vendor == 'nvidia':
            info['supported_codecs'] = list(self.ENCODERS['nvidia'].keys())
            
            # Get GPU memory
            try:
                result = subprocess.run(
                    ['nvidia-smi', '--query-gpu=memory.total', '--format=csv,noheader'],
                    capture_output=True,
                    text=True,
                    timeout=5
                )
                if result.returncode == 0:
                    info['memory'] = result.stdout.strip()
            except:
                pass
        
        elif self.gpu_vendor == 'amd':
            info['supported_codecs'] = list(self.ENCODERS['amd'].keys())
        
        elif self.gpu_vendor == 'intel':
            info['supported_codecs'] = list(self.ENCODERS['intel'].keys())
        
        elif self.gpu_vendor == 'apple':
            info['supported_codecs'] = list(self.ENCODERS['apple'].keys())
        
        return info
    
    def _build_gpu_encode_command(
        self,
        input_file: str,
        output_file: str,
        encoder: str,
        preset: str,
        quality: int
    ) -> List[str]:
        """Build FFmpeg command for GPU encoding"""
        
        cmd = [
            'ffmpeg',
            '-hwaccel', 'auto',
            '-i', input_file,
            '-c:v', encoder
        ]
        
        # Add encoder-specific options
        if 'nvenc' in encoder:
            cmd.extend([
                '-preset', preset,
                '-cq', str(quality),
                '-b:v', '0'
            ])
        elif 'amf' in encoder:
            cmd.extend([
                '-quality', preset,
                '-rc', 'cqp',
                '-qp_i', str(quality),
                '-qp_p', str(quality)
            ])
        elif 'qsv' in encoder:
            cmd.extend([
                '-preset', preset,
                '-global_quality', str(quality)
            ])
        elif 'videotoolbox' in encoder:
            cmd.extend([
                '-q:v', str(quality)
            ])
        
        cmd.extend([
            '-c:a', 'copy',
            '-y', output_file
        ])
        
        return cmd
    
    def _encode_cpu(
        self,
        input_file: str,
        output_file: str,
        codec: str,
        quality: int
    ) -> bool:
        """Fallback CPU encoding"""
        
        cpu_encoders = {
            'h264': 'libx264',
            'h265': 'libx265',
            'av1': 'libaom-av1'
        }
        
        encoder = cpu_encoders.get(codec, 'libx264')
        
        cmd = [
            'ffmpeg', '-i', input_file,
            '-c:v', encoder,
            '-crf', str(quality),
            '-c:a', 'copy',
            '-y', output_file
        ]
        
        try:
            subprocess.run(cmd, check=True, capture_output=True)
            return True
        except:
            return False
    
    def _create_test_video(self) -> str:
        """Create test video for benchmarking"""
        test_file = 'test_benchmark.mp4'
        
        cmd = [
            'ffmpeg',
            '-f', 'lavfi',
            '-i', 'testsrc=duration=10:size=1920x1080:rate=30',
            '-c:v', 'libx264',
            '-y', test_file
        ]
        
        subprocess.run(cmd, check=True, capture_output=True)
        return test_file
    
    def _benchmark_encode(
        self,
        input_file: str,
        mode: str,
        codec: str
    ) -> float:
        """Benchmark encoding time"""
        import time
        
        output_file = f'benchmark_{mode}_{codec}.mp4'
        
        start_time = time.time()
        
        if mode == 'gpu':
            self.encode_gpu(input_file, output_file, codec)
        else:
            self._encode_cpu(input_file, output_file, codec, 23)
        
        elapsed = time.time() - start_time
        
        # Cleanup
        if os.path.exists(output_file):
            os.remove(output_file)
        
        return elapsed


# CLI Integration
if __name__ == '__main__':
    print("""
    ╔══════════════════════════════════════════════════════════════╗
    ║  RSJ-FFMPEG GPU ACCELERATION MODULE                          ║
    ║  Hardware Encoding with NVIDIA, AMD, Intel, Apple           ║
    ║  By RAJSARASWATI JATAV                                      ║
    ╚══════════════════════════════════════════════════════════════╝
    """)
    
    config = {}
    engine = GPUAccelerationEngine(config)
    
    # Display GPU info
    info = engine.get_gpu_info()
    print(f"\n🎮 GPU Information:")
    print(f"  Vendor: {info['vendor']}")
    print(f"  CUDA: {info['cuda_available']}")
    print(f"  Supported Codecs: {', '.join(info['supported_codecs'])}")
    print(f"  Memory: {info['memory']}")