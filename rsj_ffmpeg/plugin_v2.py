"""
RSJ-FFMPEG Plugin System v2
Enhanced plugin architecture with hot-reload and marketplace

Author: RAJSARASWATI JATAV
Version: 2.2.0
"""

import os
import sys
import json
import importlib
import inspect
from typing import Dict, Any, List, Optional, Callable, Type
from pathlib import Path
from abc import ABC, abstractmethod
import hashlib
from datetime import datetime


class PluginV2(ABC):
    """Enhanced base plugin class"""
    
    name: str = "base_plugin"
    version: str = "1.0.0"
    author: str = "Unknown"
    description: str = ""
    dependencies: List[str] = []
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize plugin"""
        self.config = config or {}
        self.enabled = True
        self.loaded_at = datetime.now()
    
    @abstractmethod
    def process(
        self,
        input_file: str,
        output_file: str,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Process media file
        
        Args:
            input_file: Input file path
            output_file: Output file path
            **kwargs: Additional parameters
            
        Returns:
            Processing result
        """
        pass
    
    def validate(self) -> bool:
        """Validate plugin configuration"""
        return True
    
    def get_metadata(self) -> Dict[str, Any]:
        """Get plugin metadata"""
        return {
            "name": self.name,
            "version": self.version,
            "author": self.author,
            "description": self.description,
            "dependencies": self.dependencies,
            "enabled": self.enabled,
            "loaded_at": self.loaded_at.isoformat()
        }
    
    def on_load(self):
        """Called when plugin is loaded"""
        pass
    
    def on_unload(self):
        """Called when plugin is unloaded"""
        pass
    
    def on_enable(self):
        """Called when plugin is enabled"""
        self.enabled = True
    
    def on_disable(self):
        """Called when plugin is disabled"""
        self.enabled = False


class PluginManagerV2:
    """Enhanced plugin manager with hot-reload"""
    
    def __init__(self, plugins_dir: str = "./plugins"):
        """Initialize plugin manager"""
        self.plugins_dir = Path(plugins_dir)
        self.plugins_dir.mkdir(exist_ok=True)
        
        self.plugins: Dict[str, PluginV2] = {}
        self.plugin_classes: Dict[str, Type[PluginV2]] = {}
        self.plugin_files: Dict[str, str] = {}
        self.plugin_hashes: Dict[str, str] = {}
        
        # Marketplace
        self.marketplace_url = "https://rsj-ffmpeg-plugins.com/api"
        self.installed_plugins = self._load_installed_list()
    
    def discover_plugins(self) -> List[str]:
        """Discover available plugins"""
        discovered = []
        
        # Add plugins directory to path
        if str(self.plugins_dir) not in sys.path:
            sys.path.insert(0, str(self.plugins_dir))
        
        # Find all Python files
        for file in self.plugins_dir.glob("*.py"):
            if file.stem.startswith("_"):
                continue
            
            discovered.append(file.stem)
        
        return discovered
    
    def load_plugin(self, plugin_name: str) -> bool:
        """
        Load a plugin
        
        Args:
            plugin_name: Plugin module name
            
        Returns:
            Success status
        """
        try:
            # Import module
            if plugin_name in sys.modules:
                module = importlib.reload(sys.modules[plugin_name])
            else:
                module = importlib.import_module(plugin_name)
            
            # Find plugin class
            plugin_class = None
            for name, obj in inspect.getmembers(module):
                if (inspect.isclass(obj) and 
                    issubclass(obj, PluginV2) and 
                    obj != PluginV2):
                    plugin_class = obj
                    break
            
            if not plugin_class:
                print(f"⚠️  No plugin class found in {plugin_name}")
                return False
            
            # Instantiate plugin
            plugin = plugin_class()
            
            # Validate
            if not plugin.validate():
                print(f"⚠️  Plugin validation failed: {plugin_name}")
                return False
            
            # Store plugin
            self.plugins[plugin.name] = plugin
            self.plugin_classes[plugin.name] = plugin_class
            self.plugin_files[plugin.name] = str(
                self.plugins_dir / f"{plugin_name}.py"
            )
            
            # Calculate file hash
            self.plugin_hashes[plugin.name] = self._calculate_hash(
                self.plugin_files[plugin.name]
            )
            
            # Call on_load
            plugin.on_load()
            
            print(f"✅ Loaded plugin: {plugin.name} v{plugin.version}")
            return True
            
        except Exception as e:
            print(f"❌ Failed to load plugin {plugin_name}: {e}")
            return False
    
    def unload_plugin(self, plugin_name: str) -> bool:
        """Unload a plugin"""
        if plugin_name not in self.plugins:
            return False
        
        try:
            plugin = self.plugins[plugin_name]
            plugin.on_unload()
            
            del self.plugins[plugin_name]
            del self.plugin_classes[plugin_name]
            del self.plugin_files[plugin_name]
            del self.plugin_hashes[plugin_name]
            
            print(f"✅ Unloaded plugin: {plugin_name}")
            return True
            
        except Exception as e:
            print(f"❌ Failed to unload plugin {plugin_name}: {e}")
            return False
    
    def reload_plugin(self, plugin_name: str) -> bool:
        """Hot-reload a plugin"""
        if plugin_name in self.plugins:
            self.unload_plugin(plugin_name)
        
        # Find module name from plugin name
        module_name = None
        for name, pname in self.plugin_files.items():
            if name == plugin_name:
                module_name = Path(pname).stem
                break
        
        if module_name:
            return self.load_plugin(module_name)
        
        return False
    
    def load_all(self):
        """Load all discovered plugins"""
        plugins = self.discover_plugins()
        
        print(f"📦 Discovered {len(plugins)} plugins")
        
        for plugin in plugins:
            self.load_plugin(plugin)
    
    def check_updates(self) -> List[str]:
        """Check for plugin file changes"""
        updated = []
        
        for plugin_name, file_path in self.plugin_files.items():
            current_hash = self._calculate_hash(file_path)
            
            if current_hash != self.plugin_hashes.get(plugin_name):
                updated.append(plugin_name)
        
        return updated
    
    def auto_reload(self):
        """Auto-reload changed plugins"""
        updated = self.check_updates()
        
        for plugin_name in updated:
            print(f"🔄 Auto-reloading: {plugin_name}")
            self.reload_plugin(plugin_name)
    
    def execute_plugin(
        self,
        plugin_name: str,
        input_file: str,
        output_file: str,
        **kwargs
    ) -> Dict[str, Any]:
        """Execute a plugin"""
        if plugin_name not in self.plugins:
            return {
                "status": "failed",
                "error": f"Plugin not found: {plugin_name}"
            }
        
        plugin = self.plugins[plugin_name]
        
        if not plugin.enabled:
            return {
                "status": "failed",
                "error": f"Plugin disabled: {plugin_name}"
            }
        
        try:
            result = plugin.process(input_file, output_file, **kwargs)
            return {
                "status": "success",
                "plugin": plugin_name,
                "result": result
            }
        except Exception as e:
            return {
                "status": "failed",
                "error": str(e)
            }
    
    def get_plugin(self, plugin_name: str) -> Optional[PluginV2]:
        """Get plugin instance"""
        return self.plugins.get(plugin_name)
    
    def list_plugins(self) -> List[Dict[str, Any]]:
        """List all loaded plugins"""
        return [
            plugin.get_metadata()
            for plugin in self.plugins.values()
        ]
    
    def enable_plugin(self, plugin_name: str) -> bool:
        """Enable a plugin"""
        if plugin_name in self.plugins:
            self.plugins[plugin_name].on_enable()
            return True
        return False
    
    def disable_plugin(self, plugin_name: str) -> bool:
        """Disable a plugin"""
        if plugin_name in self.plugins:
            self.plugins[plugin_name].on_disable()
            return True
        return False
    
    def _calculate_hash(self, file_path: str) -> str:
        """Calculate file hash"""
        try:
            with open(file_path, 'rb') as f:
                return hashlib.md5(f.read()).hexdigest()
        except:
            return ""
    
    def _load_installed_list(self) -> List[str]:
        """Load list of installed plugins"""
        manifest_file = self.plugins_dir / "installed.json"
        
        if manifest_file.exists():
            with open(manifest_file, 'r') as f:
                return json.load(f)
        
        return []
    
    def _save_installed_list(self):
        """Save list of installed plugins"""
        manifest_file = self.plugins_dir / "installed.json"
        
        with open(manifest_file, 'w') as f:
            json.dump(self.installed_plugins, f, indent=2)
    
    # Marketplace features
    def search_marketplace(self, query: str) -> List[Dict[str, Any]]:
        """Search plugin marketplace"""
        # Placeholder - would connect to actual marketplace API
        return [
            {
                "name": "watermark_pro",
                "version": "1.0.0",
                "author": "RAJSARASWATI JATAV",
                "description": "Advanced watermarking plugin",
                "downloads": 1500,
                "rating": 4.8
            },
            {
                "name": "ai_upscaler",
                "version": "2.0.0",
                "author": "Community",
                "description": "AI-powered upscaling",
                "downloads": 3200,
                "rating": 4.9
            }
        ]
    
    def install_from_marketplace(
        self,
        plugin_name: str,
        version: Optional[str] = None
    ) -> bool:
        """Install plugin from marketplace"""
        print(f"📥 Installing {plugin_name}...")
        
        # Placeholder - would download from marketplace
        # For now, just mark as installed
        if plugin_name not in self.installed_plugins:
            self.installed_plugins.append(plugin_name)
            self._save_installed_list()
        
        print(f"✅ Installed {plugin_name}")
        return True
    
    def uninstall_plugin(self, plugin_name: str) -> bool:
        """Uninstall a plugin"""
        # Unload if loaded
        if plugin_name in self.plugins:
            self.unload_plugin(plugin_name)
        
        # Remove from installed list
        if plugin_name in self.installed_plugins:
            self.installed_plugins.remove(plugin_name)
            self._save_installed_list()
        
        # Delete file
        plugin_file = self.plugins_dir / f"{plugin_name}.py"
        if plugin_file.exists():
            plugin_file.unlink()
        
        print(f"✅ Uninstalled {plugin_name}")
        return True
    
    def check_dependencies(self, plugin_name: str) -> Dict[str, bool]:
        """Check plugin dependencies"""
        if plugin_name not in self.plugins:
            return {}
        
        plugin = self.plugins[plugin_name]
        dependencies = {}
        
        for dep in plugin.dependencies:
            try:
                importlib.import_module(dep)
                dependencies[dep] = True
            except ImportError:
                dependencies[dep] = False
        
        return dependencies
    
    def install_dependencies(self, plugin_name: str) -> bool:
        """Install plugin dependencies"""
        deps = self.check_dependencies(plugin_name)
        missing = [dep for dep, installed in deps.items() if not installed]
        
        if not missing:
            return True
        
        print(f"📦 Installing dependencies: {', '.join(missing)}")
        
        # Use pip to install
        import subprocess
        try:
            subprocess.run(
                [sys.executable, "-m", "pip", "install"] + missing,
                check=True
            )
            return True
        except:
            return False


# Example plugin template
class ExamplePlugin(PluginV2):
    """Example plugin implementation"""
    
    name = "example_plugin"
    version = "1.0.0"
    author = "RAJSARASWATI JATAV"
    description = "Example plugin for demonstration"
    dependencies = []
    
    def process(
        self,
        input_file: str,
        output_file: str,
        **kwargs
    ) -> Dict[str, Any]:
        """Process video file"""
        # Example: Add watermark
        import subprocess
        
        watermark_text = kwargs.get('watermark', 'Example Plugin')
        
        cmd = [
            "ffmpeg", "-i", input_file,
            "-vf", f"drawtext=text='{watermark_text}':x=10:y=10:fontsize=24:fontcolor=white",
            "-c:a", "copy",
            "-y", output_file
        ]
        
        try:
            subprocess.run(cmd, check=True, capture_output=True)
            return {
                "status": "success",
                "message": "Watermark added"
            }
        except Exception as e:
            return {
                "status": "failed",
                "error": str(e)
            }