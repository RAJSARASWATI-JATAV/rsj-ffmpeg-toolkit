"""
RSJ-FFMPEG Power Toolkit Setup
Installation script for the ultimate multimedia automation framework
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README
readme_file = Path(__file__).parent / "RSJ-FFMPEG-TOOLKIT.md"
long_description = readme_file.read_text(encoding='utf-8') if readme_file.exists() else ""

setup(
    name="rsj-ffmpeg",
    version="2.2.0",
    author="RAJSARASWATI JATAV",
    author_email="rajsaraswatijatav@example.com",
    description="Ultimate AI-Powered Multimedia Automation Framework",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/RAJSARASWATI-JATAV/rsj-ffmpeg-toolkit",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Multimedia :: Video",
        "Topic :: Multimedia :: Sound/Audio",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=[
        "click>=8.0.0",
        "rich>=10.0.0",
        "colorama>=0.4.4",
        "fastapi>=0.68.0",
        "uvicorn>=0.15.0",
        "pydantic>=1.8.0",
        "python-telegram-bot>=13.7",
        "discord.py>=1.7.3",
        "opencv-python>=4.5.3",
        "Pillow>=8.3.0",
        "numpy>=1.21.0",
        "requests>=2.26.0",
        "python-dotenv>=0.19.0",
        "watchdog>=2.1.5",
        "schedule>=1.1.0",
        "PyYAML>=5.4.1",
        "tqdm>=4.62.0",
    ],
    extras_require={
        "ai": [
            "torch>=1.9.0",
            "torchvision>=0.10.0",
        ],
        "dev": [
            "pytest>=6.2.0",
            "black>=21.0",
            "flake8>=3.9.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "rsj-ffmpeg=cli:main",
        ],
    },
    include_package_data=True,
    package_data={
        "rsj_ffmpeg": ["*.json", "templates/*"],
    },
    keywords="ffmpeg video audio processing ai automation streaming rsj rajsaraswati-jatav",
    project_urls={
        "Bug Reports": "https://github.com/RAJSARASWATI-JATAV/rsj-ffmpeg-toolkit/issues",
        "Source": "https://github.com/RAJSARASWATI-JATAV/rsj-ffmpeg-toolkit",
        "Documentation": "https://github.com/RAJSARASWATI-JATAV/rsj-ffmpeg-toolkit/blob/main/RSJ-FFMPEG-TOOLKIT.md",
    },
)