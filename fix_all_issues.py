#!/usr/bin/env python3
"""
RSJ-FFMPEG Toolkit - Automatic Issue Fixer
Fixes common installation and configuration issues

Author: RAJSARASWATI JATAV
Version: 2.2.0
"""

import os
import sys
import subprocess
import json
from pathlib import Path

print("""
╔══════════════════════════════════════════════════════════════╗
║  RSJ-FFMPEG TOOLKIT - AUTOMATIC ISSUE FIXER                  ║
║  Author: RAJSARASWATI JATAV                                  ║
╚══════════════════════════════════════════════════════════════╝
""")

def run_command(cmd, description):
    """Run a command and return success status"""
    print(f"\n🔧 {description}...")
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"   ✅ Success!")
            return True
        else:
            print(f"   ⚠️  Warning: {result.stderr[:100]}")
            return False
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")
        return False

def check_file_exists(filepath, description):
    """Check if a file exists"""
    if Path(filepath).exists():
        print(f"✅ {description}: Found")
        return True
    else:
        print(f"❌ {description}: Missing")
        return False

def create_env_file():
    """Create .env file if missing"""
    env_path = Path(".env")
    if not env_path.exists():
        print("\n📝 Creating .env file...")
        env_content = """# RSJ-FFMPEG Configuration
# Add your API keys here

# OpenAI (for GPT Director)
OPENAI_API_KEY=

# Cloud Providers
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
GCP_PROJECT_ID=
AZURE_STORAGE_CONNECTION_STRING=

# Bots
TELEGRAM_BOT_TOKEN=
DISCORD_BOT_TOKEN=
"""
        env_path.write_text(env_content)
        print("   ✅ .env file created")
    else:
        print("✅ .env file already exists")

def fix_config_json():
    """Ensure config.json is valid"""
    config_path = Path("config.json")
    if config_path.exists():
        try:
            with open(config_path, 'r') as f:
                config = json.load(f)
            print("✅ config.json is valid")
            return True
        except json.JSONDecodeError:
            print("⚠️  config.json has errors, backing up and creating new one")
            config_path.rename("config.json.backup")
            create_default_config()
    else:
        print("📝 Creating config.json...")
        create_default_config()

def create_default_config():
    """Create default config.json"""
    config = {
        "version": "2.2.0",
        "branding": {
            "author": "RAJSARASWATI JATAV",
            "watermark": "© RAJSARASWATI JATAV 2025"
        },
        "defaults": {
            "video_codec": "libx264",
            "audio_codec": "aac",
            "quality": "high",
            "parallel_jobs": 4
        },
        "features": {
            "batch_processing": True,
            "ai_enhancement": True,
            "streaming": True,
            "plugin_system": True
        }
    }
    with open("config.json", 'w') as f:
        json.dump(config, f, indent=2)
    print("   ✅ config.json created")

def create_directories():
    """Create necessary directories"""
    dirs = ['input', 'output', 'logs', 'reports', 'temp', 'plugins', 'uploads']
    print("\n📁 Creating directories...")
    for dir_name in dirs:
        Path(dir_name).mkdir(exist_ok=True)
    print("   ✅ All directories created")

def check_ffmpeg():
    """Check if FFmpeg is installed"""
    print("\n🎬 Checking FFmpeg...")
    result = subprocess.run("ffmpeg -version", shell=True, capture_output=True)
    if result.returncode == 0:
        print("   ✅ FFmpeg is installed")
        return True
    else:
        print("   ❌ FFmpeg not found!")
        print("   📥 Install FFmpeg:")
        print("      Windows: Download from https://ffmpeg.org")
        print("      Linux: sudo apt install ffmpeg")
        print("      Mac: brew install ffmpeg")
        return False

def main():
    """Main fixer function"""
    print("\n" + "="*60)
    print("RUNNING AUTOMATIC FIXES")
    print("="*60)
    
    # 1. Check critical files
    print("\n📋 Checking critical files...")
    check_file_exists("setup.py", "setup.py")
    check_file_exists("requirements.txt", "requirements.txt")
    check_file_exists("rsj_ffmpeg/__init__.py", "rsj_ffmpeg package")
    
    # 2. Fix config files
    print("\n⚙️  Fixing configuration files...")
    create_env_file()
    fix_config_json()
    
    # 3. Create directories
    create_directories()
    
    # 4. Check FFmpeg
    check_ffmpeg()
    
    # 5. Test imports
    print("\n🧪 Testing imports...")
    try:
        from rsj_ffmpeg import RSJToolkit
        print("   ✅ Core imports working")
    except ImportError as e:
        print(f"   ⚠️  Import issue: {e}")
        print("   💡 Run: pip install -e .")
    
    # 6. Check optional dependencies
    print("\n📦 Checking optional dependencies...")
    optional_deps = {
        'flask': 'Dashboard',
        'openai': 'AI Features',
        'boto3': 'Cloud Processing',
        'librosa': 'Audio Analysis',
        'psutil': 'System Monitoring'
    }
    
    missing_deps = []
    for dep, feature in optional_deps.items():
        try:
            __import__(dep)
            print(f"   ✅ {dep:15} - {feature}")
        except ImportError:
            print(f"   ⚠️  {dep:15} - {feature} (not installed)")
            missing_deps.append(dep)
    
    # Summary
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    
    if missing_deps:
        print(f"\n⚠️  {len(missing_deps)} optional dependencies missing:")
        for dep in missing_deps:
            print(f"   - {dep}")
        print("\n💡 Install with:")
        print(f"   pip install {' '.join(missing_deps)}")
    else:
        print("\n✅ All optional dependencies installed!")
    
    print("\n🎯 Next Steps:")
    print("   1. Run: python verify_installation.py")
    print("   2. Try: python cli.py --version")
    print("   3. Read: QUICK_FIX_GUIDE.md")
    
    print("\n" + "="*60)
    print("✅ AUTOMATIC FIXES COMPLETE!")
    print("="*60)

if __name__ == "__main__":
    main()