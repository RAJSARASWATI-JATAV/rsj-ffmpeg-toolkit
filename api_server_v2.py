#!/usr/bin/env python3
"""
RSJ-FFMPEG API Server v2
Enhanced REST API with v2.2 features

Author: RAJSARASWATI JATAV
Version: 2.2.0
"""

try:
    from fastapi import FastAPI, HTTPException, BackgroundTasks, UploadFile, File, Header
    from fastapi.responses import JSONResponse, FileResponse, StreamingResponse
    from fastapi.middleware.cors import CORSMiddleware
    from pydantic import BaseModel
    import uvicorn
except ImportError:
    print("⚠️  FastAPI not installed. Install with: pip install fastapi uvicorn")
    exit(1)

from typing import Optional, Dict, Any, List
from pathlib import Path
import uuid
from datetime import datetime
import os

from rsj_ffmpeg import (
    RSJToolkit,
    GPTDirector,
    MontageEngine,
    CloudProcessor,
    ContentAnalyzer
)
from automation.scheduler_v2 import AdvancedScheduler, Priority


# Initialize FastAPI app
app = FastAPI(
    title="RSJ-FFMPEG API v2",
    description="Ultimate AI-Powered Multimedia Automation API",
    version="2.2.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize components
toolkit = RSJToolkit()
gpt_director = GPTDirector(config={})
montage_engine = MontageEngine(config={})
content_analyzer = ContentAnalyzer(config={})
scheduler = AdvancedScheduler()

# Start scheduler
scheduler.start()

# Job storage
jobs = {}
uploads_dir = Path("./uploads")
uploads_dir.mkdir(exist_ok=True)


# Request Models
class GPTEditRequest(BaseModel):
    input_files: List[str]
    prompt: str
    output: str
    style: Optional[str] = None
    duration: Optional[int] = None
    music: Optional[str] = None


class MontageRequest(BaseModel):
    input_dir: str
    output: str
    style: str = "cinematic"
    duration: Optional[int] = None
    music: Optional[str] = None
    watermark: Optional[str] = None


class CloudProcessRequest(BaseModel):
    input_file: str
    provider: str = "aws"
    operations: List[Dict[str, Any]]
    output_bucket: str
    output_key: Optional[str] = None


class AnalyzeRequest(BaseModel):
    video_file: str
    analyze_scenes: bool = True
    analyze_audio: bool = True
    analyze_quality: bool = True
    analyze_content: bool = True


class ScheduleJobRequest(BaseModel):
    job_type: str
    parameters: Dict[str, Any]
    priority: str = "normal"
    schedule: Optional[str] = None


# API Endpoints

@app.get("/")
async def root():
    """API root endpoint"""
    return {
        "name": "RSJ-FFMPEG API v2",
        "version": "2.2.0",
        "author": "RAJSARASWATI JATAV",
        "status": "operational",
        "features": {
            "gpt_editing": True,
            "auto_montage": True,
            "cloud_processing": True,
            "content_analysis": True,
            "advanced_scheduling": True
        },
        "endpoints": {
            "v2": {
                "gpt_edit": "/api/v2/gpt/edit",
                "montage": "/api/v2/montage/create",
                "cloud": "/api/v2/cloud/process",
                "analyze": "/api/v2/analyze",
                "schedule": "/api/v2/schedule"
            }
        }
    }


@app.get("/api/v2/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "scheduler": {
            "running": scheduler.running,
            "stats": scheduler.get_statistics()
        }
    }


# GPT Director Endpoints

@app.post("/api/v2/gpt/edit")
async def gpt_edit(request: GPTEditRequest, background_tasks: BackgroundTasks):
    """GPT-powered video editing"""
    job_id = str(uuid.uuid4())
    
    def process():
        result = gpt_director.edit_from_prompt(
            input_files=request.input_files,
            prompt=request.prompt,
            output=request.output,
            style=request.style,
            duration=request.duration,
            music=request.music
        )
        jobs[job_id] = result
    
    background_tasks.add_task(process)
    
    return {
        "job_id": job_id,
        "status": "processing",
        "message": "GPT editing started"
    }


@app.post("/api/v2/gpt/analyze")
async def gpt_analyze(request: AnalyzeRequest):
    """Analyze video content"""
    result = gpt_director.analyze_content(
        video_file=request.video_file,
        analyze_audio=request.analyze_audio,
        detect_scenes=request.analyze_scenes
    )
    
    return result


# Montage Engine Endpoints

@app.post("/api/v2/montage/create")
async def create_montage(request: MontageRequest, background_tasks: BackgroundTasks):
    """Create automatic montage"""
    job_id = str(uuid.uuid4())
    
    def process():
        result = montage_engine.create_auto_montage(
            input_dir=request.input_dir,
            output=request.output,
            style=request.style,
            duration=request.duration,
            music=request.music,
            watermark=request.watermark
        )
        jobs[job_id] = result
    
    background_tasks.add_task(process)
    
    return {
        "job_id": job_id,
        "status": "processing",
        "message": "Montage creation started"
    }


@app.get("/api/v2/montage/styles")
async def list_montage_styles():
    """List available montage styles"""
    return {
        "styles": list(montage_engine.styles.keys()),
        "descriptions": {
            name: config.get("description", "")
            for name, config in montage_engine.styles.items()
        }
    }


# Cloud Processing Endpoints

@app.post("/api/v2/cloud/process")
async def cloud_process(request: CloudProcessRequest):
    """Process video in cloud"""
    cloud = CloudProcessor(
        provider=request.provider,
        credentials={}  # Should be configured
    )
    
    result = cloud.process_video(
        input_file=request.input_file,
        operations=request.operations,
        output_bucket=request.output_bucket,
        output_key=request.output_key
    )
    
    return result


@app.get("/api/v2/cloud/status/{job_id}")
async def cloud_status(job_id: str):
    """Get cloud job status"""
    # Would need to track cloud processor instances
    return {
        "job_id": job_id,
        "status": "unknown",
        "message": "Cloud job tracking not implemented"
    }


# Content Analysis Endpoints

@app.post("/api/v2/analyze")
async def analyze_content(request: AnalyzeRequest):
    """Analyze video content"""
    result = content_analyzer.analyze_video(
        video_file=request.video_file,
        analyze_scenes=request.analyze_scenes,
        analyze_audio=request.analyze_audio,
        analyze_quality=request.analyze_quality,
        analyze_content=request.analyze_content
    )
    
    return result


@app.post("/api/v2/analyze/classify")
async def classify_video(video_file: str):
    """Classify video type"""
    result = content_analyzer.classify_video(video_file)
    return result


@app.post("/api/v2/analyze/suggest")
async def suggest_improvements(video_file: str):
    """Get improvement suggestions"""
    suggestions = content_analyzer.suggest_improvements(video_file)
    return {"suggestions": suggestions}


# Scheduler Endpoints

@app.post("/api/v2/schedule")
async def schedule_job(request: ScheduleJobRequest):
    """Schedule a job"""
    priority_map = {
        "low": Priority.LOW,
        "normal": Priority.NORMAL,
        "high": Priority.HIGH,
        "critical": Priority.CRITICAL
    }
    
    job_id = str(uuid.uuid4())
    
    # Create job function based on type
    def job_function():
        # Placeholder - would execute based on job_type
        return {"status": "completed"}
    
    scheduler.schedule_job(
        job_id=job_id,
        function=job_function,
        priority=priority_map.get(request.priority, Priority.NORMAL),
        schedule=request.schedule
    )
    
    return {
        "job_id": job_id,
        "status": "scheduled"
    }


@app.get("/api/v2/schedule/jobs")
async def list_scheduled_jobs():
    """List all scheduled jobs"""
    return {
        "jobs": scheduler.list_jobs(),
        "statistics": scheduler.get_statistics()
    }


@app.get("/api/v2/schedule/jobs/{job_id}")
async def get_job_status(job_id: str):
    """Get job status"""
    status = scheduler.get_job_status(job_id)
    
    if not status:
        raise HTTPException(status_code=404, detail="Job not found")
    
    return status


@app.delete("/api/v2/schedule/jobs/{job_id}")
async def cancel_job(job_id: str):
    """Cancel a scheduled job"""
    success = scheduler.cancel_job(job_id)
    
    if not success:
        raise HTTPException(status_code=404, detail="Job not found or cannot be cancelled")
    
    return {"status": "cancelled", "job_id": job_id}


# Job Management

@app.get("/api/v2/jobs/{job_id}")
async def get_job(job_id: str):
    """Get job result"""
    if job_id not in jobs:
        raise HTTPException(status_code=404, detail="Job not found")
    
    return jobs[job_id]


@app.get("/api/v2/jobs")
async def list_jobs():
    """List all jobs"""
    return {
        "total": len(jobs),
        "jobs": list(jobs.keys())
    }


# File Upload

@app.post("/api/v2/upload")
async def upload_file(file: UploadFile = File(...)):
    """Upload a file"""
    file_path = uploads_dir / file.filename
    
    with open(file_path, "wb") as f:
        content = await file.read()
        f.write(content)
    
    return {
        "filename": file.filename,
        "path": str(file_path),
        "size": len(content)
    }


if __name__ == "__main__":
    print("🚀 Starting RSJ-FFMPEG API Server v2...")
    print("📚 Documentation: http://localhost:8080/docs")
    print("🔄 ReDoc: http://localhost:8080/redoc")
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8080,
        log_level="info"
    )