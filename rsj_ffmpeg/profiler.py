#!/usr/bin/env python3
"""
RSJ-FFMPEG Performance Profiler
Execution profiling, bottleneck detection, and optimization suggestions

Author: RAJSARASWATI JATAV
Version: 2.1.0
"""

import os
import time
import json
import psutil
import subprocess
from typing import Dict, List, Optional, Callable
from datetime import datetime
from pathlib import Path


class PerformanceProfiler:
    """Performance profiling and optimization"""
    
    def __init__(self, config: Dict):
        self.config = config
        self.profiles = []
        self.current_profile = None
    
    def start_profile(self, operation_name: str) -> str:
        """
        Start profiling an operation
        
        Args:
            operation_name: Name of operation
            
        Returns:
            Profile ID
        """
        profile_id = f"{operation_name}_{int(time.time())}"
        
        self.current_profile = {
            'id': profile_id,
            'operation': operation_name,
            'start_time': time.time(),
            'start_cpu': psutil.cpu_percent(interval=0.1),
            'start_memory': psutil.virtual_memory().percent,
            'metrics': []
        }
        
        print(f"📊 Started profiling: {operation_name}")
        return profile_id
    
    def record_metric(
        self,
        metric_name: str,
        value: float,
        unit: str = ''
    ) -> None:
        """
        Record a metric during profiling
        
        Args:
            metric_name: Metric name
            value: Metric value
            unit: Unit of measurement
        """
        if self.current_profile:
            self.current_profile['metrics'].append({
                'name': metric_name,
                'value': value,
                'unit': unit,
                'timestamp': time.time()
            })
    
    def end_profile(self) -> Dict:
        """
        End current profiling session
        
        Returns:
            Profile results
        """
        if not self.current_profile:
            print("⚠️ No active profile")
            return {}
        
        self.current_profile['end_time'] = time.time()
        self.current_profile['end_cpu'] = psutil.cpu_percent(interval=0.1)
        self.current_profile['end_memory'] = psutil.virtual_memory().percent
        
        # Calculate duration
        duration = self.current_profile['end_time'] - self.current_profile['start_time']
        self.current_profile['duration'] = duration
        
        # Calculate resource usage
        self.current_profile['avg_cpu'] = (
            self.current_profile['start_cpu'] + self.current_profile['end_cpu']
        ) / 2
        self.current_profile['avg_memory'] = (
            self.current_profile['start_memory'] + self.current_profile['end_memory']
        ) / 2
        
        # Store profile
        self.profiles.append(self.current_profile)
        
        print(f"✅ Profile complete: {self.current_profile['operation']}")
        print(f"   Duration: {duration:.2f}s")
        print(f"   Avg CPU: {self.current_profile['avg_cpu']:.1f}%")
        print(f"   Avg Memory: {self.current_profile['avg_memory']:.1f}%")
        
        result = self.current_profile
        self.current_profile = None
        
        return result
    
    def profile_function(
        self,
        func: Callable,
        *args,
        **kwargs
    ) -> tuple:
        """
        Profile a function execution
        
        Args:
            func: Function to profile
            *args: Function arguments
            **kwargs: Function keyword arguments
            
        Returns:
            (result, profile_data)
        """
        operation_name = func.__name__
        profile_id = self.start_profile(operation_name)
        
        try:
            result = func(*args, **kwargs)
            profile_data = self.end_profile()
            return result, profile_data
        except Exception as e:
            self.end_profile()
            raise e
    
    def profile_ffmpeg_command(
        self,
        cmd: List[str],
        operation_name: str = 'ffmpeg'
    ) -> Dict:
        """
        Profile FFmpeg command execution
        
        Args:
            cmd: FFmpeg command
            operation_name: Operation name
            
        Returns:
            Profile data
        """
        profile_id = self.start_profile(operation_name)
        
        # Start process
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True
        )
        
        # Monitor process
        peak_cpu = 0
        peak_memory = 0
        
        while process.poll() is None:
            try:
                proc = psutil.Process(process.pid)
                cpu = proc.cpu_percent(interval=0.1)
                memory = proc.memory_percent()
                
                peak_cpu = max(peak_cpu, cpu)
                peak_memory = max(peak_memory, memory)
                
                self.record_metric('cpu', cpu, '%')
                self.record_metric('memory', memory, '%')
            except:
                pass
            
            time.sleep(0.5)
        
        # Get output
        stdout, stderr = process.communicate()
        
        # Record peaks
        self.record_metric('peak_cpu', peak_cpu, '%')
        self.record_metric('peak_memory', peak_memory, '%')
        
        profile_data = self.end_profile()
        profile_data['stdout'] = stdout
        profile_data['stderr'] = stderr
        profile_data['return_code'] = process.returncode
        
        return profile_data
    
    def analyze_bottlenecks(
        self,
        profile_data: Optional[Dict] = None
    ) -> Dict:
        """
        Analyze performance bottlenecks
        
        Args:
            profile_data: Profile data (None = use last profile)
            
        Returns:
            Bottleneck analysis
        """
        if profile_data is None:
            if not self.profiles:
                print("⚠️ No profiles available")
                return {}
            profile_data = self.profiles[-1]
        
        analysis = {
            'operation': profile_data['operation'],
            'duration': profile_data['duration'],
            'bottlenecks': [],
            'recommendations': []
        }
        
        # Check CPU usage
        if profile_data['avg_cpu'] > 80:
            analysis['bottlenecks'].append({
                'type': 'cpu',
                'severity': 'high',
                'value': profile_data['avg_cpu'],
                'description': 'High CPU usage detected'
            })
            analysis['recommendations'].append(
                'Consider using GPU acceleration or reducing quality settings'
            )
        
        # Check memory usage
        if profile_data['avg_memory'] > 80:
            analysis['bottlenecks'].append({
                'type': 'memory',
                'severity': 'high',
                'value': profile_data['avg_memory'],
                'description': 'High memory usage detected'
            })
            analysis['recommendations'].append(
                'Consider processing in smaller chunks or reducing resolution'
            )
        
        # Check duration
        if profile_data['duration'] > 60:
            analysis['bottlenecks'].append({
                'type': 'time',
                'severity': 'medium',
                'value': profile_data['duration'],
                'description': 'Long processing time'
            })
            analysis['recommendations'].append(
                'Consider using faster presets or hardware acceleration'
            )
        
        return analysis
    
    def generate_report(
        self,
        output_file: Optional[str] = None,
        format: str = 'json'
    ) -> str:
        """
        Generate performance report
        
        Args:
            output_file: Output file path
            format: Report format (json/markdown)
            
        Returns:
            Report content or file path
        """
        if not self.profiles:
            print("⚠️ No profiles to report")
            return ""
        
        if format == 'json':
            report = self._generate_json_report()
        else:
            report = self._generate_markdown_report()
        
        if output_file:
            with open(output_file, 'w') as f:
                f.write(report)
            print(f"✅ Report saved: {output_file}")
            return output_file
        
        return report
    
    def compare_profiles(
        self,
        profile_ids: List[str]
    ) -> Dict:
        """
        Compare multiple profiles
        
        Args:
            profile_ids: List of profile IDs
            
        Returns:
            Comparison data
        """
        profiles_to_compare = [
            p for p in self.profiles if p['id'] in profile_ids
        ]
        
        if len(profiles_to_compare) < 2:
            print("⚠️ Need at least 2 profiles to compare")
            return {}
        
        comparison = {
            'profiles': profiles_to_compare,
            'fastest': min(profiles_to_compare, key=lambda p: p['duration']),
            'slowest': max(profiles_to_compare, key=lambda p: p['duration']),
            'avg_duration': sum(p['duration'] for p in profiles_to_compare) / len(profiles_to_compare)
        }
        
        return comparison
    
    def get_optimization_suggestions(
        self,
        profile_data: Optional[Dict] = None
    ) -> List[str]:
        """
        Get optimization suggestions
        
        Args:
            profile_data: Profile data
            
        Returns:
            List of suggestions
        """
        if profile_data is None:
            if not self.profiles:
                return []
            profile_data = self.profiles[-1]
        
        suggestions = []
        
        # CPU-based suggestions
        if profile_data['avg_cpu'] > 80:
            suggestions.append("🚀 Enable GPU acceleration for faster processing")
            suggestions.append("⚙️ Use faster encoding presets (e.g., 'fast' instead of 'slow')")
        
        # Memory-based suggestions
        if profile_data['avg_memory'] > 80:
            suggestions.append("💾 Process videos in smaller segments")
            suggestions.append("📉 Reduce output resolution or quality")
        
        # Duration-based suggestions
        if profile_data['duration'] > 60:
            suggestions.append("⏱️ Consider batch processing during off-hours")
            suggestions.append("🔧 Use two-pass encoding for better efficiency")
        
        # General suggestions
        suggestions.append("📊 Enable caching to avoid reprocessing")
        suggestions.append("🎯 Use appropriate codecs for your target platform")
        
        return suggestions
    
    def _generate_json_report(self) -> str:
        """Generate JSON report"""
        report = {
            'generated': datetime.now().isoformat(),
            'total_profiles': len(self.profiles),
            'profiles': self.profiles,
            'summary': {
                'total_duration': sum(p['duration'] for p in self.profiles),
                'avg_cpu': sum(p['avg_cpu'] for p in self.profiles) / len(self.profiles),
                'avg_memory': sum(p['avg_memory'] for p in self.profiles) / len(self.profiles)
            }
        }
        
        return json.dumps(report, indent=2)
    
    def _generate_markdown_report(self) -> str:
        """Generate Markdown report"""
        report = f"""# RSJ-FFMPEG Performance Report
**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
**By:** RAJSARASWATI JATAV

## Summary
- **Total Profiles:** {len(self.profiles)}
- **Total Duration:** {sum(p['duration'] for p in self.profiles):.2f}s
- **Avg CPU:** {sum(p['avg_cpu'] for p in self.profiles) / len(self.profiles):.1f}%
- **Avg Memory:** {sum(p['avg_memory'] for p in self.profiles) / len(self.profiles):.1f}%

## Profiles

"""
        
        for profile in self.profiles:
            report += f"""### {profile['operation']}
- **Duration:** {profile['duration']:.2f}s
- **CPU:** {profile['avg_cpu']:.1f}%
- **Memory:** {profile['avg_memory']:.1f}%

"""
        
        return report


# CLI Integration
if __name__ == '__main__':
    print("""
    ╔══════════════════════════════════════════════════════════════╗
    ║  RSJ-FFMPEG PERFORMANCE PROFILER                             ║
    ║  Execution Profiling & Optimization Suggestions              ║
    ║  By RAJSARASWATI JATAV                                      ║
    ╚══════════════════════════════════════════════════════════════╝
    """)
    
    config = {}
    profiler = PerformanceProfiler(config)
    
    print("\n📊 Available Methods:")
    print("  • start_profile() - Start profiling")
    print("  • end_profile() - End profiling")
    print("  • profile_function() - Profile a function")
    print("  • profile_ffmpeg_command() - Profile FFmpeg")
    print("  • analyze_bottlenecks() - Analyze bottlenecks")
    print("  • get_optimization_suggestions() - Get suggestions")
    print("  • generate_report() - Generate report")