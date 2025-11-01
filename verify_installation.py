#!/usr/bin/env python3
"""
RSJ-FFMPEG v2.2 Installation Verification
Quick test to verify all components are working

Author: RAJSARASWATI JATAV
Version: 2.2.0
"""

import sys

def test_imports():
    """Test if all modules can be imported"""
    print("🔍 Testing imports...")
    
    try:
        from rsj_ffmpeg import RSJToolkit
        print("  ✅ RSJToolkit")
    except Exception as e:
        print(f"  ❌ RSJToolkit: {e}")
        return False
    
    try:
        from rsj_ffmpeg import GPTDirector
        print("  ✅ GPTDirector")
    except Exception as e:
        print(f"  ❌ GPTDirector: {e}")
        return False
    
    try:
        from rsj_ffmpeg import CloudProcessor
        print("  ✅ CloudProcessor")
    except Exception as e:
        print(f"  ❌ CloudProcessor: {e}")
        return False
    
    try:
        from rsj_ffmpeg import MontageEngine
        print("  ✅ MontageEngine")
    except Exception as e:
        print(f"  ❌ MontageEngine: {e}")
        return False
    
    try:
        from rsj_ffmpeg import ContentAnalyzer
        print("  ✅ ContentAnalyzer")
    except Exception as e:
        print(f"  ❌ ContentAnalyzer: {e}")
        return False
    
    return True


def test_initialization():
    """Test if classes can be initialized"""
    print("\n🔧 Testing initialization...")
    
    try:
        from rsj_ffmpeg import RSJToolkit
        toolkit = RSJToolkit()
        print(f"  ✅ RSJToolkit v{toolkit.version}")
    except Exception as e:
        print(f"  ❌ RSJToolkit init: {e}")
        return False
    
    try:
        from rsj_ffmpeg import GPTDirector
        director = GPTDirector(config={})
        print("  ✅ GPTDirector initialized")
    except Exception as e:
        print(f"  ❌ GPTDirector init: {e}")
        return False
    
    try:
        from rsj_ffmpeg import CloudProcessor
        cloud = CloudProcessor(provider="aws", credentials={})
        print("  ✅ CloudProcessor initialized")
    except Exception as e:
        print(f"  ❌ CloudProcessor init: {e}")
        return False
    
    try:
        from rsj_ffmpeg import MontageEngine
        engine = MontageEngine(config={})
        styles = engine.get_available_styles()
        print(f"  ✅ MontageEngine ({len(styles)} styles available)")
    except Exception as e:
        print(f"  ❌ MontageEngine init: {e}")
        return False
    
    try:
        from rsj_ffmpeg import ContentAnalyzer
        analyzer = ContentAnalyzer(config={})
        print("  ✅ ContentAnalyzer initialized")
    except Exception as e:
        print(f"  ❌ ContentAnalyzer init: {e}")
        return False
    
    return True


def check_dependencies():
    """Check if key dependencies are installed"""
    print("\n📦 Checking dependencies...")
    
    deps = {
        "click": "CLI framework",
        "rich": "Terminal formatting",
        "fastapi": "API server",
        "flask": "Dashboard server",
        "psutil": "System monitoring"
    }
    
    all_ok = True
    for dep, desc in deps.items():
        try:
            __import__(dep)
            print(f"  ✅ {dep:20s} - {desc}")
        except ImportError:
            print(f"  ⚠️  {dep:20s} - {desc} (not installed)")
            all_ok = False
    
    # Optional dependencies
    print("\n  Optional dependencies:")
    optional = {
        "openai": "GPT Director",
        "boto3": "AWS Cloud Processing",
        "librosa": "Beat detection",
        "GPUtil": "GPU monitoring"
    }
    
    for dep, desc in optional.items():
        try:
            __import__(dep)
            print(f"  ✅ {dep:20s} - {desc}")
        except ImportError:
            print(f"  ℹ️  {dep:20s} - {desc} (optional)")
    
    return all_ok


def main():
    """Run all verification tests"""
    print("=" * 60)
    print("☠️  RSJ-FFMPEG v2.2 INSTALLATION VERIFICATION  ☠️")
    print("=" * 60)
    print()
    
    # Test imports
    if not test_imports():
        print("\n❌ Import test failed!")
        sys.exit(1)
    
    # Test initialization
    if not test_initialization():
        print("\n❌ Initialization test failed!")
        sys.exit(1)
    
    # Check dependencies
    check_dependencies()
    
    print("\n" + "=" * 60)
    print("✅ ALL TESTS PASSED!")
    print("=" * 60)
    print()
    print("🎉 RSJ-FFMPEG v2.2 is ready to use!")
    print()
    print("📚 Next steps:")
    print("  1. Try examples: python examples/gpt_editing.py")
    print("  2. Start dashboard: python dashboard/analytics_v2.py")
    print("  3. Read docs: docs/v2.2_guide.md")
    print()
    print("Built with 💀 by RAJSARASWATI JATAV")
    print()


if __name__ == "__main__":
    main()