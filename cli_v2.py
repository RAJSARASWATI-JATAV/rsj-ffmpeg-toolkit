#!/usr/bin/env python3
"""
RSJ-FFMPEG CLI v2
Enhanced command-line interface with v2.2 features

Author: RAJSARASWATI JATAV
Version: 2.2.0
"""

import click
from rich.console import Console
from rich.table import Table
from rich.progress import Progress
from rich.panel import Panel
from rich import print as rprint
import os
import sys

from rsj_ffmpeg import (
    RSJToolkit,
    GPTDirector,
    MontageEngine,
    CloudProcessor,
    ContentAnalyzer,
    BANNER
)
from rsj_ffmpeg.video_templates import VideoTemplates

console = Console()


@click.group()
@click.version_option(version="2.2.0")
def cli():
    """
    ☠️ RSJ-FFMPEG Power Toolkit v2.2 ☠️
    
    Ultimate AI-Powered Multimedia Automation
    
    Author: RAJSARASWATI JATAV
    """
    console.print(BANNER, style="bold cyan")


# GPT Director Commands

@cli.group()
def gpt():
    """GPT-powered video editing"""
    pass


@gpt.command()
@click.option('-i', '--input', 'input_files', multiple=True, required=True, help='Input video files')
@click.option('-o', '--output', required=True, help='Output file')
@click.option('-p', '--prompt', required=True, help='Editing prompt')
@click.option('-s', '--style', help='Editing style')
@click.option('-d', '--duration', type=int, help='Target duration (seconds)')
@click.option('-m', '--music', help='Background music file')
@click.option('--api-key', envvar='OPENAI_API_KEY', help='OpenAI API key')
def edit(input_files, output, prompt, style, duration, music, api_key):
    """Edit video using natural language"""
    console.print(f"\n🎬 GPT Director: Editing with prompt...", style="bold green")
    console.print(f"📝 Prompt: {prompt}\n")
    
    director = GPTDirector(config={}, api_key=api_key)
    
    with Progress() as progress:
        task = progress.add_task("[cyan]Processing...", total=100)
        
        result = director.edit_from_prompt(
            input_files=list(input_files),
            prompt=prompt,
            output=output,
            style=style,
            duration=duration,
            music=music
        )
        
        progress.update(task, completed=100)
    
    if result['status'] == 'success':
        console.print(f"\n✅ Success! Output: {result['output']}", style="bold green")
    else:
        console.print(f"\n❌ Failed: {result.get('error')}", style="bold red")


@gpt.command()
@click.option('-i', '--input', required=True, help='Video file to analyze')
@click.option('--scenes/--no-scenes', default=True, help='Detect scenes')
@click.option('--audio/--no-audio', default=True, help='Analyze audio')
def analyze(input, scenes, audio):
    """Analyze video content"""
    console.print(f"\n🔍 Analyzing: {input}\n", style="bold cyan")
    
    director = GPTDirector(config={})
    analysis = director.analyze_content(
        video_file=input,
        analyze_audio=audio,
        detect_scenes=scenes
    )
    
    # Display results
    table = Table(title="Analysis Results")
    table.add_column("Property", style="cyan")
    table.add_column("Value", style="green")
    
    table.add_row("Duration", f"{analysis.get('duration', 0):.2f}s")
    table.add_row("Scenes Detected", str(len(analysis.get('scenes', []))))
    table.add_row("Has Audio", str(analysis.get('audio_analysis', {}).get('has_audio', False)))
    
    console.print(table)


# Montage Commands

@cli.group()
def montage():
    """Automatic montage creation"""
    pass


@montage.command()
@click.option('-i', '--input-dir', required=True, help='Input directory with clips')
@click.option('-o', '--output', required=True, help='Output file')
@click.option('-s', '--style', default='cinematic', help='Montage style')
@click.option('-d', '--duration', type=int, help='Target duration (seconds)')
@click.option('-m', '--music', help='Background music')
@click.option('-w', '--watermark', help='Watermark text')
def create(input_dir, output, style, duration, music, watermark):
    """Create automatic montage"""
    console.print(f"\n🎬 Creating {style} montage...\n", style="bold green")
    
    engine = MontageEngine(config={})
    
    with Progress() as progress:
        task = progress.add_task("[cyan]Creating montage...", total=100)
        
        result = engine.create_auto_montage(
            input_dir=input_dir,
            output=output,
            style=style,
            duration=duration,
            music=music,
            watermark=watermark
        )
        
        progress.update(task, completed=100)
    
    if result['status'] == 'success':
        console.print(f"\n✅ Montage created: {result['output']}", style="bold green")
        console.print(f"🎬 Clips used: {result['clips_used']}")
    else:
        console.print(f"\n❌ Failed: {result.get('error')}", style="bold red")


@montage.command()
def styles():
    """List available montage styles"""
    engine = MontageEngine(config={})
    
    table = Table(title="Available Montage Styles")
    table.add_column("Style", style="cyan")
    table.add_column("Pace", style="yellow")
    table.add_column("Transitions", style="green")
    
    for name, config in engine.styles.items():
        table.add_row(
            name,
            config.get('pace', 'medium'),
            ', '.join(config.get('transitions', []))
        )
    
    console.print(table)


# Cloud Commands

@cli.group()
def cloud():
    """Cloud processing"""
    pass


@cloud.command()
@click.option('-i', '--input', required=True, help='Input file')
@click.option('-p', '--provider', default='aws', help='Cloud provider')
@click.option('-b', '--bucket', required=True, help='Output bucket')
@click.option('-o', '--output-key', help='Output key')
def process(input, provider, bucket, output_key):
    """Process video in cloud"""
    console.print(f"\n☁️  Processing in {provider.upper()}...\n", style="bold cyan")
    
    cloud_proc = CloudProcessor(provider=provider, credentials={})
    
    result = cloud_proc.process_video(
        input_file=input,
        operations=[{"type": "compress", "bitrate": "5M"}],
        output_bucket=bucket,
        output_key=output_key
    )
    
    if result.get('status') == 'submitted':
        console.print(f"\n✅ Job submitted: {result.get('job_id')}", style="bold green")
    else:
        console.print(f"\n❌ Failed: {result.get('error')}", style="bold red")


# Analysis Commands

@cli.group()
def analyze_cmd():
    """Content analysis"""
    pass


@analyze_cmd.command()
@click.option('-i', '--input', required=True, help='Video file')
def full(input):
    """Full content analysis"""
    console.print(f"\n🔍 Analyzing: {input}\n", style="bold cyan")
    
    analyzer = ContentAnalyzer(config={})
    
    with Progress() as progress:
        task = progress.add_task("[cyan]Analyzing...", total=100)
        
        analysis = analyzer.analyze_video(input)
        
        progress.update(task, completed=100)
    
    # Display results
    console.print(Panel.fit(
        f"[bold]Duration:[/bold] {analysis['metadata']['duration']:.2f}s\n"
        f"[bold]Resolution:[/bold] {analysis['metadata']['video']['width']}x{analysis['metadata']['video']['height']}\n"
        f"[bold]Scenes:[/bold] {len(analysis['scenes'])}\n"
        f"[bold]Quality Score:[/bold] {analysis['quality']['overall_score']:.2f}",
        title="Analysis Results",
        border_style="green"
    ))


@analyze_cmd.command()
@click.option('-i', '--input', required=True, help='Video file')
def classify(input):
    """Classify video type"""
    analyzer = ContentAnalyzer(config={})
    classification = analyzer.classify_video(input)
    
    console.print(Panel.fit(
        f"[bold]Type:[/bold] {classification['type']}\n"
        f"[bold]Confidence:[/bold] {classification['confidence']:.2%}\n"
        f"[bold]Recommendations:[/bold]\n" +
        "\n".join(f"  • {rec}" for rec in classification['recommendations']),
        title="Classification",
        border_style="cyan"
    ))


# Template Commands

@cli.group()
def template():
    """Video templates"""
    pass


@template.command()
@click.option('-t', '--type', 'template_type', required=True, help='Template type')
@click.option('-o', '--output', required=True, help='Output file')
@click.option('--title', help='Title text')
@click.option('-i', '--input', help='Input video (if required)')
def create_template(template_type, output, title, input):
    """Create from template"""
    templates = VideoTemplates(config={})
    
    console.print(f"\n🎨 Creating {template_type} template...\n", style="bold cyan")
    
    if template_type == "youtube_intro":
        result = templates.create_youtube_intro(output, title or "My Channel")
    elif template_type == "youtube_outro":
        result = templates.create_youtube_outro(output, title or "My Channel")
    elif template_type == "instagram_story" and input:
        result = templates.create_instagram_story(input, output, title)
    else:
        console.print("❌ Invalid template or missing parameters", style="bold red")
        return
    
    if result['status'] == 'success':
        console.print(f"✅ Template created: {output}", style="bold green")
    else:
        console.print(f"❌ Failed: {result.get('error')}", style="bold red")


@template.command()
def list_templates():
    """List available templates"""
    templates = VideoTemplates(config={})
    
    table = Table(title="Available Templates")
    table.add_column("Template", style="cyan")
    table.add_column("Resolution", style="yellow")
    table.add_column("Duration", style="green")
    
    for name, info in templates.templates.items():
        table.add_row(
            name,
            info.get('resolution', 'N/A'),
            f"{info.get('duration', 0)}s"
        )
    
    console.print(table)


if __name__ == "__main__":
    cli()