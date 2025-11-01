#!/usr/bin/env python3
"""
RSJ-FFMPEG Scheduler
Schedule automated video processing tasks
"""

try:
    import schedule
except ImportError:
    print("⚠️  schedule not installed. Install with: pip install schedule")
    exit(1)

import time
import argparse
from pathlib import Path
from datetime import datetime
from rsj_ffmpeg import RSJToolkit, BANNER
from rsj_ffmpeg.utils import generate_report


class TaskScheduler:
    """Schedule and run automated tasks"""
    
    def __init__(self, toolkit: RSJToolkit):
        self.toolkit = toolkit
        self.tasks = []
    
    def add_batch_task(
        self,
        name: str,
        input_dir: str,
        output_dir: str,
        schedule_time: str,
        **options
    ):
        """Add a scheduled batch processing task"""
        def task():
            print(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Running task: {name}")
            
            try:
                result = self.toolkit.batch_convert(
                    input_dir=input_dir,
                    output_dir=output_dir,
                    **options
                )
                
                print(f"✅ Task completed: {name}")
                print(f"   Processed: {result['summary']['completed']} files")
                
                # Generate report
                report_path = generate_report(
                    result['jobs'],
                    format='json',
                    output_file=f"reports/{name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                )
                print(f"   Report: {report_path}")
                
            except Exception as e:
                print(f"❌ Task failed: {name}")
                print(f"   Error: {e}")
        
        # Schedule task
        if schedule_time == "hourly":
            schedule.every().hour.do(task)
        elif schedule_time == "daily":
            schedule.every().day.at("02:00").do(task)
        elif schedule_time.startswith("every_"):
            # e.g., "every_30_minutes"
            interval = int(schedule_time.split('_')[1])
            unit = schedule_time.split('_')[2]
            
            if unit == "minutes":
                schedule.every(interval).minutes.do(task)
            elif unit == "hours":
                schedule.every(interval).hours.do(task)
        else:
            # Specific time (HH:MM)
            schedule.every().day.at(schedule_time).do(task)
        
        self.tasks.append({
            "name": name,
            "schedule": schedule_time,
            "task": task
        })
        
        print(f"✅ Scheduled task: {name} ({schedule_time})")
    
    def run(self):
        """Run scheduler"""
        print("\n⏰ Scheduler started")
        print(f"📋 Active tasks: {len(self.tasks)}")
        
        for task in self.tasks:
            print(f"   - {task['name']}: {task['schedule']}")
        
        print("\nPress Ctrl+C to stop\n")
        
        try:
            while True:
                schedule.run_pending()
                time.sleep(60)  # Check every minute
        except KeyboardInterrupt:
            print("\n\n⚠️  Stopping scheduler...")
            print("✅ Stopped\n")


def main():
    """Main scheduler"""
    parser = argparse.ArgumentParser(
        description="RSJ-FFMPEG Task Scheduler"
    )
    
    parser.add_argument('--config', help='Configuration file (JSON)')
    
    args = parser.parse_args()
    
    print(BANNER)
    print("\n⏰ RSJ-FFMPEG Task Scheduler\n")
    
    # Initialize
    toolkit = RSJToolkit()
    scheduler = TaskScheduler(toolkit)
    
    # Example tasks (in production, load from config file)
    if args.config:
        # Load tasks from config
        import json
        with open(args.config) as f:
            config = json.load(f)
            
        for task in config.get('tasks', []):
            scheduler.add_batch_task(**task)
    else:
        # Default example tasks
        scheduler.add_batch_task(
            name="Daily Batch Processing",
            input_dir="./input/daily/",
            output_dir="./output/daily/",
            schedule_time="02:00",
            ai_upscale="2x",
            enhance=True,
            watermark="RAJSARASWATI JATAV"
        )
        
        scheduler.add_batch_task(
            name="Hourly Quick Convert",
            input_dir="./input/quick/",
            output_dir="./output/quick/",
            schedule_time="hourly",
            format="mp4"
        )
    
    # Run scheduler
    scheduler.run()
    
    print("© 2025 RAJSARASWATI JATAV | All Rights Reserved")


if __name__ == "__main__":
    main()