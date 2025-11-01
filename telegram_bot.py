#!/usr/bin/env python3
"""
RSJ-FFMPEG Telegram Bot
Control RSJ-FFMPEG via Telegram
"""

try:
    from telegram import Update
    from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
except ImportError:
    print("⚠️  python-telegram-bot not installed. Install with: pip install python-telegram-bot")
    exit(1)

import os
from pathlib import Path
from rsj_ffmpeg import RSJToolkit, BANNER

# Initialize toolkit
toolkit = RSJToolkit()
downloads_dir = Path("./bot_downloads")
downloads_dir.mkdir(exist_ok=True)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start command"""
    welcome_message = f"""
{BANNER}

🤖 **RSJ-FFMPEG Telegram Bot**
Ultimate Multimedia Automation

**Available Commands:**
/start - Show this message
/convert - Convert video format
/enhance - AI enhance video
/watermark - Add watermark
/gif - Create GIF
/audio - Extract audio
/info - Get video info
/help - Show detailed help

**Usage:**
1. Send me a video file
2. Use commands to process it
3. Get your result!

© 2025 RAJSARASWATI JATAV
    """
    await update.message.reply_text(welcome_message)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Help command"""
    help_text = """
📚 **RSJ-FFMPEG Bot Help**

**Commands:**

/convert <format>
Convert video to specified format
Example: /convert mp4

/enhance
Apply AI enhancement to video
- Upscaling
- Denoising
- Color correction

/watermark <text>
Add watermark to video
Example: /watermark RAJSARASWATI JATAV

/gif
Convert video to GIF

/audio
Extract audio from video

/info
Get video information

**How to use:**
1. Send a video file
2. Reply to the video with a command
3. Wait for processing
4. Download result

**Support:**
Telegram: @rajsaraswatijatav
GitHub: RAJSARASWATI-JATAV
    """
    await update.message.reply_text(help_text)


async def handle_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle video uploads"""
    video = update.message.video or update.message.document
    
    if not video:
        await update.message.reply_text("❌ Please send a video file")
        return
    
    await update.message.reply_text("📥 Downloading video...")
    
    # Download video
    file = await context.bot.get_file(video.file_id)
    file_path = downloads_dir / f"{video.file_id}.mp4"
    await file.download_to_drive(file_path)
    
    # Store file path in context
    context.user_data['last_video'] = str(file_path)
    
    await update.message.reply_text(
        f"✅ Video downloaded!\n\n"
        f"Now you can use commands:\n"
        f"/convert mp4\n"
        f"/enhance\n"
        f"/watermark YOUR_TEXT\n"
        f"/gif\n"
        f"/audio"
    )


async def convert_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Convert video format"""
    if 'last_video' not in context.user_data:
        await update.message.reply_text("❌ Please send a video first")
        return
    
    # Get format from command args
    format_type = context.args[0] if context.args else "mp4"
    
    input_file = context.user_data['last_video']
    output_file = str(Path(input_file).with_suffix(f'.{format_type}'))
    
    await update.message.reply_text(f"🔄 Converting to {format_type}...")
    
    try:
        # Convert
        result = toolkit.batch_convert(
            input_dir=str(Path(input_file).parent),
            output_dir=str(Path(output_file).parent),
            format=format_type
        )
        
        # Send result
        await update.message.reply_video(
            video=open(output_file, 'rb'),
            caption=f"✅ Converted to {format_type}\n© RAJSARASWATI JATAV"
        )
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {str(e)}")


async def enhance_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Enhance video with AI"""
    if 'last_video' not in context.user_data:
        await update.message.reply_text("❌ Please send a video first")
        return
    
    input_file = context.user_data['last_video']
    output_file = str(Path(input_file).with_stem(f"{Path(input_file).stem}_enhanced"))
    
    await update.message.reply_text("🎨 Enhancing video with AI...")
    
    try:
        result = toolkit.ai_enhance(
            input_file=input_file,
            output_file=output_file,
            upscale=2,
            denoise=True
        )
        
        await update.message.reply_video(
            video=open(output_file, 'rb'),
            caption="✅ AI Enhanced\n© RAJSARASWATI JATAV"
        )
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {str(e)}")


async def watermark_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Add watermark to video"""
    if 'last_video' not in context.user_data:
        await update.message.reply_text("❌ Please send a video first")
        return
    
    watermark_text = " ".join(context.args) if context.args else "RAJSARASWATI JATAV"
    
    input_file = context.user_data['last_video']
    output_file = str(Path(input_file).with_stem(f"{Path(input_file).stem}_watermarked"))
    
    await update.message.reply_text(f"🏷️ Adding watermark: {watermark_text}")
    
    try:
        result = toolkit.add_watermark(
            input_file=input_file,
            output_file=output_file,
            watermark_text=watermark_text
        )
        
        await update.message.reply_video(
            video=open(output_file, 'rb'),
            caption=f"✅ Watermark added\n© RAJSARASWATI JATAV"
        )
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {str(e)}")


async def gif_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Create GIF from video"""
    if 'last_video' not in context.user_data:
        await update.message.reply_text("❌ Please send a video first")
        return
    
    input_file = context.user_data['last_video']
    output_file = str(Path(input_file).with_suffix('.gif'))
    
    await update.message.reply_text("🎞️ Creating GIF...")
    
    try:
        result = toolkit.create_gif(
            input_file=input_file,
            output_file=output_file,
            duration=5,
            fps=15
        )
        
        await update.message.reply_animation(
            animation=open(output_file, 'rb'),
            caption="✅ GIF created\n© RAJSARASWATI JATAV"
        )
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {str(e)}")


async def audio_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Extract audio from video"""
    if 'last_video' not in context.user_data:
        await update.message.reply_text("❌ Please send a video first")
        return
    
    input_file = context.user_data['last_video']
    output_file = str(Path(input_file).with_suffix('.mp3'))
    
    await update.message.reply_text("🎵 Extracting audio...")
    
    try:
        result = toolkit.extract_audio(
            input_file=input_file,
            output_file=output_file
        )
        
        await update.message.reply_audio(
            audio=open(output_file, 'rb'),
            caption="✅ Audio extracted\n© RAJSARASWATI JATAV"
        )
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {str(e)}")


async def info_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Get video information"""
    if 'last_video' not in context.user_data:
        await update.message.reply_text("❌ Please send a video first")
        return
    
    input_file = context.user_data['last_video']
    
    try:
        info = toolkit.get_video_info(input_file)
        
        if 'format' in info:
            format_info = info['format']
            message = f"""
📊 **Video Information**

**File:** {Path(input_file).name}
**Duration:** {format_info.get('duration', 'N/A')}s
**Size:** {int(format_info.get('size', 0)) / (1024*1024):.1f} MB
**Format:** {format_info.get('format_name', 'N/A')}

© RAJSARASWATI JATAV
            """
        else:
            message = "❌ Could not retrieve video information"
        
        await update.message.reply_text(message)
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {str(e)}")


def main():
    """Run Telegram bot"""
    print(BANNER)
    print("\n🤖 Starting RSJ-FFMPEG Telegram Bot...")
    
    # Get bot token from environment
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    
    if not token:
        print("❌ TELEGRAM_BOT_TOKEN environment variable not set")
        print("Set it with: export TELEGRAM_BOT_TOKEN='your_token_here'")
        return
    
    # Create application
    application = Application.builder().token(token).build()
    
    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("convert", convert_command))
    application.add_handler(CommandHandler("enhance", enhance_command))
    application.add_handler(CommandHandler("watermark", watermark_command))
    application.add_handler(CommandHandler("gif", gif_command))
    application.add_handler(CommandHandler("audio", audio_command))
    application.add_handler(CommandHandler("info", info_command))
    
    # Handle video uploads
    application.add_handler(MessageHandler(
        filters.VIDEO | filters.Document.VIDEO,
        handle_video
    ))
    
    print("✅ Bot started successfully!")
    print("📱 Send /start to your bot to begin")
    print("\n© 2025 RAJSARASWATI JATAV | All Rights Reserved\n")
    
    # Run bot
    application.run_polling()


if __name__ == "__main__":
    main()