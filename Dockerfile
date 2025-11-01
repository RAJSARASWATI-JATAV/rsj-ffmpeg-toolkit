# RSJ-FFMPEG Power Toolkit Docker Image
# © 2025 RAJSARASWATI JATAV

FROM python:3.11-slim

# Metadata
LABEL maintainer="RAJSARASWATI JATAV"
LABEL description="RSJ-FFMPEG Ultimate AI-Powered Multimedia Automation Framework"
LABEL version="2.0.0"

# Install system dependencies
RUN apt-get update && apt-get install -y \
    ffmpeg \
    git \
    curl \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Install package
RUN pip install -e .

# Create directories
RUN mkdir -p input output logs reports temp plugins uploads

# Expose API port
EXPOSE 8080

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV RSJ_FFMPEG_VERSION=2.0.0

# Default command (API server)
CMD ["python3", "api_server.py"]

# Alternative commands:
# CLI: docker run rsj-ffmpeg rsj-ffmpeg --help
# Telegram Bot: docker run -e TELEGRAM_BOT_TOKEN=xxx rsj-ffmpeg python3 telegram_bot.py
# Discord Bot: docker run -e DISCORD_BOT_TOKEN=xxx rsj-ffmpeg python3 discord_bot.py