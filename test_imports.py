#!/usr/bin/env python3
"""
Test all imports and identify missing dependencies
"""

import sys
import importlib

def test_import(module_name, package=None):
    """Test if a module can be imported"""
    try:
        if package:
            mod = importlib.import_module(f"{package}.{module_name}")
        else:
            mod = importlib.import_module(module_name)
        return True, None
    except ImportError as e:
        return False, str(e)
    except Exception as e:
        return False, f"Error: {str(e)}"

print("=" * 60)
print("RSJ-FFMPEG IMPORT TEST")
print("=" * 60)

# Test core modules
print("\n📦 Testing Core Modules:")
core_modules = [
    ('rsj_ffmpeg', None),
    ('core', 'rsj_ffmpeg'),
    ('video', 'rsj_ffmpeg'),
    ('audio', 'rsj_ffmpeg'),
    ('utils', 'rsj_ffmpeg'),
    ('plugin', 'rsj_ffmpeg'),
]

for module, package in core_modules:
    success, error = test_import(module, package)
    status = "✅" if success else "❌"
    print(f"  {status} {package}.{module if package else module}")
    if not success:
        print(f"      Error: {error}")

# Test v2.2 modules
print("\n🆕 Testing v2.2 Modules:")
v22_modules = [
    ('gpt_director', 'rsj_ffmpeg'),
    ('cloud_processor', 'rsj_ffmpeg'),
    ('montage_engine', 'rsj_ffmpeg'),
    ('content_analyzer', 'rsj_ffmpeg'),
]

for module, package in v22_modules:
    success, error = test_import(module, package)
    status = "✅" if success else "❌"
    print(f"  {status} {package}.{module}")
    if not success:
        print(f"      Error: {error}")

# Test advanced modules
print("\n⚡ Testing Advanced Modules:")
advanced_modules = [
    ('ai_engine', 'rsj_ffmpeg'),
    ('streaming', 'rsj_ffmpeg'),
    ('plugin_v2', 'rsj_ffmpeg'),
    ('video_templates', 'rsj_ffmpeg'),
]

for module, package in advanced_modules:
    success, error = test_import(module, package)
    status = "✅" if success else "❌"
    print(f"  {status} {package}.{module}")
    if not success:
        print(f"      Error: {error}")

# Test optional modules (may have missing dependencies)
print("\n🔧 Testing Optional Modules (may have missing deps):")
optional_modules = [
    ('cache', 'rsj_ffmpeg'),
    ('color_grading', 'rsj_ffmpeg'),
    ('distributed', 'rsj_ffmpeg'),
    ('face_detection', 'rsj_ffmpeg'),
    ('gpu_acceleration', 'rsj_ffmpeg'),
    ('profiler', 'rsj_ffmpeg'),
    ('spatial_audio', 'rsj_ffmpeg'),
]

for module, package in optional_modules:
    success, error = test_import(module, package)
    status = "✅" if success else "⚠️"
    print(f"  {status} {package}.{module}")
    if not success:
        print(f"      Note: {error}")

# Test external dependencies
print("\n📚 Testing External Dependencies:")
dependencies = [
    'click',
    'rich',
    'fastapi',
    'uvicorn',
    'flask',
    'flask_socketio',
    'flask_cors',
    'psutil',
    'openai',
    'boto3',
    'pandas',
    'plotly',
    'librosa',
]

missing_deps = []
for dep in dependencies:
    success, error = test_import(dep)
    status = "✅" if success else "❌"
    print(f"  {status} {dep}")
    if not success:
        missing_deps.append(dep)

# Summary
print("\n" + "=" * 60)
print("SUMMARY")
print("=" * 60)
if missing_deps:
    print(f"\n⚠️  Missing {len(missing_deps)} dependencies:")
    for dep in missing_deps:
        print(f"   - {dep}")
    print("\nInstall with:")
    print(f"   pip install {' '.join(missing_deps)}")
else:
    print("\n✅ All dependencies installed!")

print("\n" + "=" * 60)