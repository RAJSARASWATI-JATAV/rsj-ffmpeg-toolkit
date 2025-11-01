#!/usr/bin/env python3
"""
RSJ-FFMPEG Advanced Scheduler v2
Cron-like scheduling with priority queues and resource management

Author: RAJSARASWATI JATAV
Version: 2.2.0
"""

import os
import json
import time
import threading
from typing import Dict, Any, List, Optional, Callable
from datetime import datetime, timedelta
from pathlib import Path
import heapq
from enum import Enum
import psutil


class Priority(Enum):
    """Job priority levels"""
    LOW = 3
    NORMAL = 2
    HIGH = 1
    CRITICAL = 0


class JobStatus(Enum):
    """Job status"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    RETRYING = "retrying"


class ScheduledJob:
    """Scheduled job with priority and retry logic"""
    
    def __init__(
        self,
        job_id: str,
        function: Callable,
        args: tuple = (),
        kwargs: dict = None,
        priority: Priority = Priority.NORMAL,
        schedule: Optional[str] = None,
        max_retries: int = 3,
        retry_delay: int = 60,
        timeout: Optional[int] = None,
        resource_requirements: Optional[Dict[str, Any]] = None
    ):
        self.job_id = job_id
        self.function = function
        self.args = args
        self.kwargs = kwargs or {}
        self.priority = priority
        self.schedule = schedule
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self.timeout = timeout
        self.resource_requirements = resource_requirements or {}
        
        self.status = JobStatus.PENDING
        self.retries = 0
        self.created_at = datetime.now()
        self.started_at = None
        self.completed_at = None
        self.result = None
        self.error = None
        self.next_run = self._calculate_next_run()
    
    def _calculate_next_run(self) -> datetime:
        """Calculate next run time based on schedule"""
        if not self.schedule:
            return datetime.now()
        
        # Parse cron-like schedule
        # Format: "*/5 * * * *" (every 5 minutes)
        # For now, simple implementation
        
        if self.schedule.startswith("every_"):
            # Format: "every_5m", "every_1h", "every_1d"
            parts = self.schedule.split("_")
            if len(parts) == 2:
                value = int(parts[1][:-1])
                unit = parts[1][-1]
                
                if unit == 'm':
                    return datetime.now() + timedelta(minutes=value)
                elif unit == 'h':
                    return datetime.now() + timedelta(hours=value)
                elif unit == 'd':
                    return datetime.now() + timedelta(days=value)
        
        return datetime.now()
    
    def __lt__(self, other):
        """Compare jobs for priority queue"""
        if self.priority.value != other.priority.value:
            return self.priority.value < other.priority.value
        return self.next_run < other.next_run


class AdvancedScheduler:
    """Advanced job scheduler with resource management"""
    
    def __init__(
        self,
        max_workers: int = 4,
        max_cpu_percent: float = 80.0,
        max_memory_percent: float = 80.0
    ):
        self.max_workers = max_workers
        self.max_cpu_percent = max_cpu_percent
        self.max_memory_percent = max_memory_percent
        
        self.jobs: Dict[str, ScheduledJob] = {}
        self.queue: List[ScheduledJob] = []
        self.running_jobs: Dict[str, threading.Thread] = {}
        
        self.running = False
        self.scheduler_thread = None
        
        # Statistics
        self.stats = {
            "total_jobs": 0,
            "completed": 0,
            "failed": 0,
            "cancelled": 0
        }
    
    def schedule_job(
        self,
        job_id: str,
        function: Callable,
        args: tuple = (),
        kwargs: dict = None,
        priority: Priority = Priority.NORMAL,
        schedule: Optional[str] = None,
        max_retries: int = 3,
        retry_delay: int = 60,
        timeout: Optional[int] = None,
        resource_requirements: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Schedule a job
        
        Args:
            job_id: Unique job identifier
            function: Function to execute
            args: Function arguments
            kwargs: Function keyword arguments
            priority: Job priority
            schedule: Cron-like schedule string
            max_retries: Maximum retry attempts
            retry_delay: Delay between retries (seconds)
            timeout: Job timeout (seconds)
            resource_requirements: Required resources
            
        Returns:
            Job ID
        """
        job = ScheduledJob(
            job_id=job_id,
            function=function,
            args=args,
            kwargs=kwargs,
            priority=priority,
            schedule=schedule,
            max_retries=max_retries,
            retry_delay=retry_delay,
            timeout=timeout,
            resource_requirements=resource_requirements
        )
        
        self.jobs[job_id] = job
        heapq.heappush(self.queue, job)
        self.stats["total_jobs"] += 1
        
        print(f"📅 Scheduled job: {job_id} (Priority: {priority.name})")
        
        return job_id
    
    def cancel_job(self, job_id: str) -> bool:
        """Cancel a scheduled job"""
        if job_id not in self.jobs:
            return False
        
        job = self.jobs[job_id]
        
        if job.status == JobStatus.RUNNING:
            # Can't cancel running job directly
            # Would need to implement thread interruption
            return False
        
        job.status = JobStatus.CANCELLED
        self.stats["cancelled"] += 1
        
        print(f"❌ Cancelled job: {job_id}")
        return True
    
    def start(self):
        """Start the scheduler"""
        if self.running:
            return
        
        self.running = True
        self.scheduler_thread = threading.Thread(target=self._scheduler_loop)
        self.scheduler_thread.daemon = True
        self.scheduler_thread.start()
        
        print("🚀 Scheduler started")
    
    def stop(self):
        """Stop the scheduler"""
        self.running = False
        
        if self.scheduler_thread:
            self.scheduler_thread.join(timeout=5)
        
        print("🛑 Scheduler stopped")
    
    def _scheduler_loop(self):
        """Main scheduler loop"""
        while self.running:
            try:
                # Check resources
                if not self._check_resources():
                    time.sleep(5)
                    continue
                
                # Check if we can run more jobs
                if len(self.running_jobs) >= self.max_workers:
                    time.sleep(1)
                    continue
                
                # Get next job
                if not self.queue:
                    time.sleep(1)
                    continue
                
                # Peek at next job
                next_job = self.queue[0]
                
                # Check if it's time to run
                if next_job.next_run > datetime.now():
                    time.sleep(1)
                    continue
                
                # Pop job from queue
                job = heapq.heappop(self.queue)
                
                # Check resource requirements
                if not self._check_job_resources(job):
                    # Re-queue with delay
                    job.next_run = datetime.now() + timedelta(seconds=30)
                    heapq.heappush(self.queue, job)
                    continue
                
                # Execute job
                self._execute_job(job)
                
            except Exception as e:
                print(f"⚠️  Scheduler error: {e}")
                time.sleep(1)
    
    def _execute_job(self, job: ScheduledJob):
        """Execute a job in a separate thread"""
        def job_wrapper():
            try:
                job.status = JobStatus.RUNNING
                job.started_at = datetime.now()
                
                print(f"▶️  Running job: {job.job_id}")
                
                # Execute function
                result = job.function(*job.args, **job.kwargs)
                
                job.status = JobStatus.COMPLETED
                job.completed_at = datetime.now()
                job.result = result
                
                self.stats["completed"] += 1
                
                print(f"✅ Completed job: {job.job_id}")
                
                # Re-schedule if recurring
                if job.schedule:
                    job.next_run = job._calculate_next_run()
                    job.status = JobStatus.PENDING
                    heapq.heappush(self.queue, job)
                
            except Exception as e:
                print(f"❌ Job failed: {job.job_id} - {e}")
                
                job.error = str(e)
                job.retries += 1
                
                # Retry logic
                if job.retries < job.max_retries:
                    job.status = JobStatus.RETRYING
                    job.next_run = datetime.now() + timedelta(seconds=job.retry_delay)
                    heapq.heappush(self.queue, job)
                    print(f"🔄 Retrying job: {job.job_id} (Attempt {job.retries + 1}/{job.max_retries})")
                else:
                    job.status = JobStatus.FAILED
                    job.completed_at = datetime.now()
                    self.stats["failed"] += 1
            
            finally:
                # Remove from running jobs
                if job.job_id in self.running_jobs:
                    del self.running_jobs[job.job_id]
        
        # Start job thread
        thread = threading.Thread(target=job_wrapper)
        thread.daemon = True
        thread.start()
        
        self.running_jobs[job.job_id] = thread
    
    def _check_resources(self) -> bool:
        """Check if system resources are available"""
        cpu_percent = psutil.cpu_percent(interval=1)
        memory_percent = psutil.virtual_memory().percent
        
        if cpu_percent > self.max_cpu_percent:
            print(f"⚠️  High CPU usage: {cpu_percent}%")
            return False
        
        if memory_percent > self.max_memory_percent:
            print(f"⚠️  High memory usage: {memory_percent}%")
            return False
        
        return True
    
    def _check_job_resources(self, job: ScheduledJob) -> bool:
        """Check if job resource requirements are met"""
        reqs = job.resource_requirements
        
        if not reqs:
            return True
        
        # Check CPU
        if "min_cpu_free" in reqs:
            cpu_free = 100 - psutil.cpu_percent(interval=1)
            if cpu_free < reqs["min_cpu_free"]:
                return False
        
        # Check memory
        if "min_memory_free_gb" in reqs:
            memory_free_gb = psutil.virtual_memory().available / (1024**3)
            if memory_free_gb < reqs["min_memory_free_gb"]:
                return False
        
        # Check disk space
        if "min_disk_free_gb" in reqs:
            disk_free_gb = psutil.disk_usage('/').free / (1024**3)
            if disk_free_gb < reqs["min_disk_free_gb"]:
                return False
        
        return True
    
    def get_job_status(self, job_id: str) -> Optional[Dict[str, Any]]:
        """Get job status"""
        if job_id not in self.jobs:
            return None
        
        job = self.jobs[job_id]
        
        return {
            "job_id": job.job_id,
            "status": job.status.value,
            "priority": job.priority.name,
            "created_at": job.created_at.isoformat(),
            "started_at": job.started_at.isoformat() if job.started_at else None,
            "completed_at": job.completed_at.isoformat() if job.completed_at else None,
            "retries": job.retries,
            "max_retries": job.max_retries,
            "next_run": job.next_run.isoformat() if job.next_run else None,
            "result": job.result,
            "error": job.error
        }
    
    def list_jobs(
        self,
        status: Optional[JobStatus] = None
    ) -> List[Dict[str, Any]]:
        """List all jobs"""
        jobs = []
        
        for job in self.jobs.values():
            if status and job.status != status:
                continue
            
            jobs.append(self.get_job_status(job.job_id))
        
        return jobs
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get scheduler statistics"""
        return {
            **self.stats,
            "queued": len(self.queue),
            "running": len(self.running_jobs),
            "success_rate": (
                self.stats["completed"] / self.stats["total_jobs"] * 100
                if self.stats["total_jobs"] > 0 else 0
            )
        }
    
    def clear_completed(self):
        """Clear completed jobs"""
        to_remove = []
        
        for job_id, job in self.jobs.items():
            if job.status in [JobStatus.COMPLETED, JobStatus.FAILED, JobStatus.CANCELLED]:
                if not job.schedule:  # Don't remove recurring jobs
                    to_remove.append(job_id)
        
        for job_id in to_remove:
            del self.jobs[job_id]
        
        print(f"🧹 Cleared {len(to_remove)} completed jobs")