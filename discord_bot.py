#!/usr/bin/env python3
"""
RSJ-FFMPEG Discord Bot
Control RSJ-FFMPEG via Discord
"""

try:
    import discord
    from discord.ext import commands
except ImportError:
    print("⚠️  discord.py not installed. Install with: pip install discord.py")
    exit(1)

import os
from pathlib import Path
from rsj_ffmpeg import RSJToolkit, BANNER

# Initialize bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!rsj ', intents=intents)

# Initialize toolkit
toolkit = RSJToolkit()
downloads_dir = Path("./bot_downloads")
downloads_dir.mkdir(exist_ok=True)


@bot.event
async def on_ready():
    """Bot ready event"""
    print(f'\n✅ {bot.user} is now online!')
    print(f'📊 Connected to {len(bot.guilds)} servers')
    print('© 2025 RAJSARASWATI JATAV\n')


@bot.command(name='start')
async def start(ctx):
    """Start command"""
    embed = discord.Embed(
        title="🔥 RSJ-FFMPEG Discord Bot",
        description="Ultimate Multimedia Automation",
        color=discord.Color.blue()
    )
    
    embed.add_field(
        name="📚 Commands",
        value="""
        `!rsj convert <format>` - Convert video
        `!rsj enhance` - AI enhance video
        `!rsj watermark <text>` - Add watermark
        `!rsj gif` - Create GIF
        `!rsj audio` - Extract audio
        `!rsj info` - Get video info
        `!rsj help` - Show help
        """,
        inline=False
    )
    
    embed.add_field(
        name="💡 Usage",
        value="Upload a video and use commands to process it!",
        inline=False
    )
    
    embed.set_footer(text="© 2025 RAJSARASWATI JATAV")
    
    await ctx.send(embed=embed)


@bot.command(name='convert')
async def convert(ctx, format_type: str = "mp4"):
    """Convert video format"""
    if not ctx.message.attachments:
        await ctx.send("❌ Please attach a video file")
        return
    
    attachment = ctx.message.attachments[0]
    
    if not attachment.content_type or 'video' not in attachment.content_type:
        await ctx.send("❌ Please attach a video file")
        return
    
    await ctx.send(f"📥 Downloading and converting to {format_type}...")
    
    # Download file
    input_file = downloads_dir / attachment.filename
    await attachment.save(input_file)
    
    output_file = input_file.with_suffix(f'.{format_type}')
    
    try:
        # Convert
        result = toolkit.batch_convert(
            input_dir=str(downloads_dir),
            output_dir=str(downloads_dir),
            format=format_type
        )
        
        # Send result
        await ctx.send(
            f"✅ Converted to {format_type}",
            file=discord.File(output_file)
        )
    except Exception as e:
        await ctx.send(f"❌ Error: {str(e)}")


@bot.command(name='enhance')
async def enhance(ctx):
    """Enhance video with AI"""
    if not ctx.message.attachments:
        await ctx.send("❌ Please attach a video file")
        return
    
    attachment = ctx.message.attachments[0]
    await ctx.send("🎨 Enhancing video with AI...")
    
    # Download file
    input_file = downloads_dir / attachment.filename
    await attachment.save(input_file)
    
    output_file = input_file.with_stem(f"{input_file.stem}_enhanced")
    
    try:
        result = toolkit.ai_enhance(
            input_file=str(input_file),
            output_file=str(output_file),
            upscale=2,
            denoise=True
        )
        
        await ctx.send(
            "✅ AI Enhanced",
            file=discord.File(output_file)
        )
    except Exception as e:
        await ctx.send(f"❌ Error: {str(e)}")


@bot.command(name='watermark')
async def watermark(ctx, *, text: str = "RAJSARASWATI JATAV"):
    """Add watermark to video"""
    if not ctx.message.attachments:
        await ctx.send("❌ Please attach a video file")
        return
    
    attachment = ctx.message.attachments[0]
    await ctx.send(f"🏷️ Adding watermark: {text}")
    
    # Download file
    input_file = downloads_dir / attachment.filename
    await attachment.save(input_file)
    
    output_file = input_file.with_stem(f"{input_file.stem}_watermarked")
    
    try:
        result = toolkit.add_watermark(
            input_file=str(input_file),
            output_file=str(output_file),
            watermark_text=text
        )
        
        await ctx.send(
            "✅ Watermark added",
            file=discord.File(output_file)
        )
    except Exception as e:
        await ctx.send(f"❌ Error: {str(e)}")


@bot.command(name='gif')
async def create_gif(ctx):
    """Create GIF from video"""
    if not ctx.message.attachments:
        await ctx.send("❌ Please attach a video file")
        return
    
    attachment = ctx.message.attachments[0]
    await ctx.send("🎞️ Creating GIF...")
    
    # Download file
    input_file = downloads_dir / attachment.filename
    await attachment.save(input_file)
    
    output_file = input_file.with_suffix('.gif')
    
    try:
        result = toolkit.create_gif(
            input_file=str(input_file),
            output_file=str(output_file),
            duration=5,
            fps=15
        )
        
        await ctx.send(
            "✅ GIF created",
            file=discord.File(output_file)
        )
    except Exception as e:
        await ctx.send(f"❌ Error: {str(e)}")


@bot.command(name='audio')
async def extract_audio(ctx):
    """Extract audio from video"""
    if not ctx.message.attachments:
        await ctx.send("❌ Please attach a video file")
        return
    
    attachment = ctx.message.attachments[0]
    await ctx.send("🎵 Extracting audio...")
    
    # Download file
    input_file = downloads_dir / attachment.filename
    await attachment.save(input_file)
    
    output_file = input_file.with_suffix('.mp3')
    
    try:
        result = toolkit.extract_audio(
            input_file=str(input_file),
            output_file=str(output_file)
        )
        
        await ctx.send(
            "✅ Audio extracted",
            file=discord.File(output_file)
        )
    except Exception as e:
        await ctx.send(f"❌ Error: {str(e)}")


@bot.command(name='info')
async def video_info(ctx):
    """Get video information"""
    if not ctx.message.attachments:
        await ctx.send("❌ Please attach a video file")
        return
    
    attachment = ctx.message.attachments[0]
    
    # Download file
    input_file = downloads_dir / attachment.filename
    await attachment.save(input_file)
    
    try:
        info = toolkit.get_video_info(str(input_file))
        
        if 'format' in info:
            format_info = info['format']
            
            embed = discord.Embed(
                title="📊 Video Information",
                color=discord.Color.green()
            )
            
            embed.add_field(name="File", value=attachment.filename, inline=False)
            embed.add_field(name="Duration", value=f"{format_info.get('duration', 'N/A')}s", inline=True)
            embed.add_field(name="Size", value=f"{int(format_info.get('size', 0)) / (1024*1024):.1f} MB", inline=True)
            embed.add_field(name="Format", value=format_info.get('format_name', 'N/A'), inline=True)
            
            embed.set_footer(text="© 2025 RAJSARASWATI JATAV")
            
            await ctx.send(embed=embed)
        else:
            await ctx.send("❌ Could not retrieve video information")
    except Exception as e:
        await ctx.send(f"❌ Error: {str(e)}")


def main():
    """Run Discord bot"""
    print(BANNER)
    print("\n🤖 Starting RSJ-FFMPEG Discord Bot...")
    
    # Get bot token from environment
    token = os.getenv("DISCORD_BOT_TOKEN")
    
    if not token:
        print("❌ DISCORD_BOT_TOKEN environment variable not set")
        print("Set it with: export DISCORD_BOT_TOKEN='your_token_here'")
        return
    
    print("© 2025 RAJSARASWATI JATAV | All Rights Reserved\n")
    
    # Run bot
    bot.run(token)


if __name__ == "__main__":
    main()