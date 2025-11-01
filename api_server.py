#!/usr/bin/env python3
"""
RSJ-FFMPEG API Server
REST API for remote control and automation
"""

try:
    from fastapi import FastAPI, HTTPException, BackgroundTasks, UploadFile, File
    from fastapi.responses import JSONResponse, FileResponse
    from pydantic import BaseModel
    import uvicorn
except ImportError:
    print("⚠️  FastAPI not installed. Install with: pip install fastapi uvicorn")
    exit(1)

from typing import Optional, Dict, Any, List
from pathlib import Path
import uuid
from datetime import datetime

from rsj_ffmpeg import RSJToolkit, BANNER
from rsj_ffmpeg.streaming import StreamManager
from rsj_ffmpeg.ai_engine import AIEngine

# Initialize FastAPI app
app = FastAPI(
    title="RSJ-FFMPEG API",
    description="Ultimate AI-Powered Multimedia Automation API",
    version="2.0.0"
)

# Initialize toolkit
toolkit = RSJToolkit()
stream_manager = StreamManager(toolkit.config)
ai_engine = AIEngine(toolkit.config)

# Job storage
jobs = {}
uploads_dir = Path("./uploads")
uploads_dir.mkdir(exist_ok=True)


# Request Models
class ConvertRequest(BaseModel):
    input_file: str
    output_file: str
    format: Optional[str] = "mp4"
    ai_upscale: Optional[str] = None
    enhance: bool = False
    watermark: Optional[str] = None


class EnhanceRequest(BaseModel):
    input_file: str
    output_file: str
    upscale: int = 2
    denoise: bool = True
    stabilize: bool = False


class StreamRequest(BaseModel):
    platform: str
    key: str
    input_source: str = "webcam"
    overlay: Optional[str] = None
    stats_overlay: bool = False
    watermark: Optional[str] = None


class BatchRequest(BaseModel):
    input_dir: str
    output_dir: str
    format: str = "mp4"
    ai_upscale: Optional[str] = None
    enhance: bool = False


# API Endpoints
@app.get("/")
async def root():
    """API root endpoint"""
    return {
        "name": "RSJ-FFMPEG API",
        "version": "2.0.0",
        "author": "RAJSARASWATI JATAV",
        "status": "operational",
        "endpoints": {
            "convert": "/api/v1/convert",
            "enhance": "/api/v1/enhance",
            "stream": "/api/v1/stream",
            "batch": "/api/v1/batch",
            "jobs": "/api/v1/jobs"
        }
    }


@app.get("/api/v1/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "2.0.0"
    }


@app.post("/api/v1/convert")
async def convert_video(request: ConvertRequest, background_tasks: BackgroundTasks):
    """Convert video with optional enhancements"""
    job_id = str(uuid.uuid4())
    
    def process():
        try:
            result = toolkit.batch_convert(
                input_dir=str(Path(request.input_file).parent),
                output_dir=str(Path(request.output_file).parent),
                format=request.format,
                ai_upscale=request.ai_upscale,
                enhance=request.enhance,
                watermark=request.watermark
            )
            jobs[job_id]["status"] = "completed"
            jobs[job_id]["result"] = result
        except Exception as e:
            jobs[job_id]["status"] = "failed"
            jobs[job_id]["error"] = str(e)
    
    jobs[job_id] = {
        "status": "processing",
        "type": "convert",
        "created_at": datetime.now().isoformat()
    }
    
    background_tasks.add_task(process)
    
    return {
        "job_id": job_id,
        "status": "processing",
        "message": "Conversion started"
    }


@app.post("/api/v1/enhance")
async def enhance_video(request: EnhanceRequest, background_tasks: BackgroundTasks):
    """AI-powered video enhancement"""
    job_id = str(uuid.uuid4())
    
    def process():
        try:
            result = toolkit.ai_enhance(
                input_file=request.input_file,
                output_file=request.output_file,
                upscale=request.upscale,
                denoise=request.denoise,
                stabilize=request.stabilize
            )
            jobs[job_id]["status"] = "completed"
            jobs[job_id]["result"] = result
        except Exception as e:
            jobs[job_id]["status"] = "failed"
            jobs[job_id]["error"] = str(e)
    
    jobs[job_id] = {
        "status": "processing",
        "type": "enhance",
        "created_at": datetime.now().isoformat()
    }
    
    background_tasks.add_task(process)
    
    return {
        "job_id": job_id,
        "status": "processing",
        "message": "Enhancement started"
    }


@app.post("/api/v1/stream/start")
async def start_stream(request: StreamRequest):
    """Start live stream"""
    stream_id = str(uuid.uuid4())
    
    result = stream_manager.start_stream(
        stream_id=stream_id,
        platform=request.platform,
        key=request.key,
        input_source=request.input_source,
        overlay=request.overlay,
        stats_overlay=request.stats_overlay,
        watermark=request.watermark
    )
    
    return {
        "stream_id": stream_id,
        **result
    }


@app.get("/api/v1/stream/{stream_id}/status")
async def get_stream_status(stream_id: str):
    """Get stream status"""
    status = stream_manager.get_stream_status(stream_id)
    return status


@app.post("/api/v1/stream/{stream_id}/stop")
async def stop_stream(stream_id: str):
    """Stop live stream"""
    result = stream_manager.stop_stream(stream_id)
    return result


@app.post("/api/v1/batch")
async def batch_process(request: BatchRequest, background_tasks: BackgroundTasks):
    """Batch process videos"""
    job_id = str(uuid.uuid4())
    
    def process():
        try:
            result = toolkit.batch_convert(
                input_dir=request.input_dir,
                output_dir=request.output_dir,
                format=request.format,
                ai_upscale=request.ai_upscale,
                enhance=request.enhance
            )
            jobs[job_id]["status"] = "completed"
            jobs[job_id]["result"] = result
        except Exception as e:
            jobs[job_id]["status"] = "failed"
            jobs[job_id]["error"] = str(e)
    
    jobs[job_id] = {
        "status": "processing",
        "type": "batch",
        "created_at": datetime.now().isoformat()
    }
    
    background_tasks.add_task(process)
    
    return {
        "job_id": job_id,
        "status": "processing",
        "message": "Batch processing started"
    }


@app.get("/api/v1/jobs")
async def list_jobs():
    """List all jobs"""
    return {
        "jobs": jobs,
        "total": len(jobs)
    }


@app.get("/api/v1/jobs/{job_id}")
async def get_job(job_id: str):
    """Get job status"""
    if job_id not in jobs:
        raise HTTPException(status_code=404, detail="Job not found")
    
    return jobs[job_id]


@app.delete("/api/v1/jobs/{job_id}")
async def delete_job(job_id: str):
    """Delete job"""
    if job_id not in jobs:
        raise HTTPException(status_code=404, detail="Job not found")
    
    del jobs[job_id]
    return {"message": "Job deleted"}


@app.post("/api/v1/upload")
async def upload_file(file: UploadFile = File(...)):
    """Upload video file"""
    file_path = uploads_dir / file.filename
    
    with open(file_path, "wb") as f:
        content = await file.read()
        f.write(content)
    
    return {
        "filename": file.filename,
        "path": str(file_path),
        "size": len(content)
    }


@app.get("/api/v1/info/{filename}")
async def get_video_info(filename: str):
    """Get video information"""
    file_path = uploads_dir / filename
    
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found")
    
    info = toolkit.get_video_info(str(file_path))
    return info


def main():
    """Run API server"""
    print(BANNER)
    print("\n🚀 Starting RSJ-FFMPEG API Server...")
    print("📡 Server: http://0.0.0.0:8080")
    print("📚 Docs: http://0.0.0.0:8080/docs")
    print("🔧 API: http://0.0.0.0:8080/api/v1/")
    print("\n© 2025 RAJSARASWATI JATAV | All Rights Reserved\n")
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8080,
        log_level="info"
    )


if __name__ == "__main__":
    main()