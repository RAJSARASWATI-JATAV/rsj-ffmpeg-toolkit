"""
RSJ-FFMPEG Plugin System
Extensible plugin architecture for custom filters
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List


class Plugin(ABC):
    """Base plugin class for custom filters"""
    
    name: str = "base_plugin"
    version: str = "1.0.0"
    
    @abstractmethod
    def process(self, input_file: str, output_file: str, **kwargs) -> Dict[str, Any]:
        """
        Process media file with custom logic
        
        Args:
            input_file: Input file path
            output_file: Output file path
            **kwargs: Additional parameters
            
        Returns:
            Processing result dictionary
        """
        pass
    
    def get_ffmpeg_args(self) -> List[str]:
        """
        Get FFmpeg arguments for this plugin
        
        Returns:
            List of FFmpeg command arguments
        """
        return []
    
    @classmethod
    def register(cls, plugin_class):
        """Register a plugin"""
        # Plugin registration logic
        print(f"Registered plugin: {plugin_class.name} v{plugin_class.version}")
        return plugin_class


class PluginManager:
    """Manage and execute plugins"""
    
    def __init__(self):
        self.plugins: Dict[str, Plugin] = {}
    
    def load_plugin(self, plugin: Plugin):
        """Load a plugin instance"""
        self.plugins[plugin.name] = plugin
    
    def execute_plugin(
        self,
        plugin_name: str,
        input_file: str,
        output_file: str,
        **kwargs
    ) -> Dict[str, Any]:
        """Execute a specific plugin"""
        if plugin_name not in self.plugins:
            return {"status": "failed", "error": f"Plugin '{plugin_name}' not found"}
        
        plugin = self.plugins[plugin_name]
        return plugin.process(input_file, output_file, **kwargs)
    
    def list_plugins(self) -> List[Dict[str, str]]:
        """List all loaded plugins"""
        return [
            {"name": name, "version": plugin.version}
            for name, plugin in self.plugins.items()
        ]


# Example custom plugin
class WatermarkPlugin(Plugin):
    """Example watermark plugin"""
    
    name = "rsj_watermark"
    version = "1.0.0"
    
    def process(self, input_file: str, output_file: str, **kwargs) -> Dict[str, Any]:
        """Add RSJ watermark to video"""
        import subprocess
        
        watermark_text = kwargs.get("text", "RAJSARASWATI JATAV")
        position = kwargs.get("position", "bottom-right")
        
        positions = {
            "top-left": "x=10:y=10",
            "top-right": "x=W-tw-10:y=10",
            "bottom-left": "x=10:y=H-th-10",
            "bottom-right": "x=W-tw-10:y=H-th-10"
        }
        
        pos = positions.get(position, positions["bottom-right"])
        
        cmd = [
            "ffmpeg", "-i", input_file,
            "-vf", f"drawtext=text='{watermark_text}':fontsize=24:fontcolor=white@0.7:{pos}",
            "-c:a", "copy",
            output_file
        ]
        
        try:
            subprocess.run(cmd, check=True, capture_output=True)
            return {"status": "success", "plugin": self.name}
        except subprocess.CalledProcessError as e:
            return {"status": "failed", "error": str(e)}
    
    def get_ffmpeg_args(self) -> List[str]:
        """Get FFmpeg arguments"""
        return ["-vf", "drawtext=text='RAJSARASWATI JATAV':fontsize=24:fontcolor=white@0.7:x=W-tw-10:y=H-th-10"]