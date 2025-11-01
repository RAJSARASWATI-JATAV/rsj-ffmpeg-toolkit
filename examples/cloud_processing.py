#!/usr/bin/env python3
"""
RSJ-FFMPEG Cloud Processing Examples
Cloud-based video processing demonstrations

Author: RAJSARASWATI JATAV
Version: 2.2.0
"""

import sys
import os
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from rsj_ffmpeg.cloud_processor import CloudProcessor


def example_1_aws_processing():
    """Example 1: Process video on AWS"""
    print("=" * 60)
    print("Example 1: AWS Cloud Processing")
    print("=" * 60)
    
    # Initialize AWS processor
    cloud = CloudProcessor(
        provider="aws",
        credentials={
            "access_key": os.getenv("AWS_ACCESS_KEY"),
            "secret_key": os.getenv("AWS_SECRET_KEY"),
            "region": "us-east-1",
            "mediaconvert_role": os.getenv("AWS_MEDIACONVERT_ROLE")
        }
    )
    
    # Process video
    result = cloud.process_video(
        input_file="large_video.mp4",
        operations=[
            {"type": "upscale", "factor": 4},
            {"type": "enhance", "preset": "cinematic"},
            {"type": "compress", "bitrate": "5M"}
        ],
        output_bucket="my-output-bucket",
        output_key="processed/video.mp4",
        callback_url="https://myapp.com/webhook"
    )
    
    print(f"\n✅ Job submitted: {result['job_id']}")
    print(f"📊 Status: {result['status']}")
    
    # Monitor job
    print("\n⏳ Monitoring job progress...")
    while True:
        status = cloud.get_job_status(result['job_id'])
        print(f"  Status: {status.get('status')} - Progress: {status.get('progress', 0)}%")
        
        if status.get('status') in ['complete', 'failed']:
            break
        
        time.sleep(10)
    
    # Download result
    if status.get('status') == 'complete':
        print("\n📥 Downloading result...")
        download = cloud.download_result(
            result['job_id'],
            "processed_video.mp4"
        )
        print(f"✅ Downloaded to: {download.get('local_path')}")


def example_2_gcp_processing():
    """Example 2: Process video on Google Cloud"""
    print("\n" + "=" * 60)
    print("Example 2: Google Cloud Processing")
    print("=" * 60)
    
    cloud = CloudProcessor(
        provider="gcp",
        credentials={
            "credentials_file": "path/to/credentials.json"
        }
    )
    
    result = cloud.process_video(
        input_file="video.mp4",
        operations=[
            {"type": "transcode", "format": "mp4"},
            {"type": "watermark", "text": "© RAJSARASWATI JATAV"}
        ],
        output_bucket="my-gcp-bucket",
        output_key="output/video.mp4"
    )
    
    print(f"\n✅ Result: {result['status']}")


def example_3_cloudflare_stream():
    """Example 3: Upload to Cloudflare Stream"""
    print("\n" + "=" * 60)
    print("Example 3: Cloudflare Stream Upload")
    print("=" * 60)
    
    cloud = CloudProcessor(
        provider="cloudflare",
        credentials={
            "api_token": os.getenv("CLOUDFLARE_API_TOKEN"),
            "account_id": os.getenv("CLOUDFLARE_ACCOUNT_ID")
        }
    )
    
    # Upload video
    result = cloud.upload_file(
        local_file="video.mp4",
        remote_path="my-video"
    )
    
    print(f"\n✅ Upload status: {result['status']}")
    if result['status'] == 'success':
        print(f"🔗 Preview URL: {result.get('url')}")
        print(f"🆔 Video UID: {result.get('uid')}")


def example_4_batch_cloud_processing():
    """Example 4: Batch process multiple videos"""
    print("\n" + "=" * 60)
    print("Example 4: Batch Cloud Processing")
    print("=" * 60)
    
    cloud = CloudProcessor(provider="aws", credentials={})
    
    videos = [
        "video1.mp4",
        "video2.mp4",
        "video3.mp4"
    ]
    
    jobs = []
    
    # Submit all jobs
    for video in videos:
        print(f"\n📤 Submitting: {video}")
        result = cloud.process_video(
            input_file=video,
            operations=[
                {"type": "compress", "bitrate": "3M"}
            ],
            output_bucket="batch-output",
            output_key=f"processed/{video}"
        )
        jobs.append(result['job_id'])
        print(f"  ✅ Job ID: {result['job_id']}")
    
    # Monitor all jobs
    print("\n⏳ Monitoring all jobs...")
    while jobs:
        for job_id in jobs[:]:
            status = cloud.get_job_status(job_id)
            if status.get('status') in ['complete', 'failed']:
                print(f"  ✅ Job {job_id}: {status.get('status')}")
                jobs.remove(job_id)
        
        if jobs:
            time.sleep(10)
    
    print("\n✅ All jobs completed!")


def example_5_cost_optimization():
    """Example 5: Cost-optimized processing"""
    print("\n" + "=" * 60)
    print("Example 5: Cost-Optimized Processing")
    print("=" * 60)
    
    # Compare costs across providers
    providers = ["aws", "gcp", "azure"]
    
    for provider in providers:
        cloud = CloudProcessor(provider=provider, credentials={})
        
        # Estimate cost (placeholder)
        print(f"\n💰 {provider.upper()} Pricing:")
        print(f"  - Transcoding: $0.015/min")
        print(f"  - Storage: $0.023/GB/month")
        print(f"  - Data transfer: $0.09/GB")


def example_6_distributed_processing():
    """Example 6: Distributed processing across nodes"""
    print("\n" + "=" * 60)
    print("Example 6: Distributed Processing")
    print("=" * 60)
    
    cloud = CloudProcessor(provider="aws", credentials={})
    
    # Split large video into chunks and process in parallel
    large_video = "very_large_video.mp4"
    chunks = 10
    
    print(f"📹 Processing {large_video} in {chunks} chunks...")
    
    jobs = []
    for i in range(chunks):
        result = cloud.process_video(
            input_file=f"{large_video}#chunk{i}",
            operations=[
                {"type": "upscale", "factor": 2}
            ],
            output_bucket="distributed-output",
            output_key=f"chunks/chunk{i}.mp4",
            priority="high"
        )
        jobs.append(result['job_id'])
    
    print(f"\n✅ Submitted {len(jobs)} parallel jobs")


def main():
    """Run all examples"""
    print("\n☁️  RSJ-FFMPEG Cloud Processing Examples")
    print("Author: RAJSARASWATI JATAV")
    print("Version: 2.2.0\n")
    
    print("⚠️  Note: Make sure you have:")
    print("  1. Cloud provider credentials set")
    print("  2. Appropriate permissions configured")
    print("  3. Billing enabled on cloud accounts\n")
    
    print("🔐 Required Environment Variables:")
    print("  AWS:")
    print("    - AWS_ACCESS_KEY")
    print("    - AWS_SECRET_KEY")
    print("    - AWS_MEDIACONVERT_ROLE")
    print("  GCP:")
    print("    - GCP_CREDENTIALS_FILE")
    print("  Cloudflare:")
    print("    - CLOUDFLARE_API_TOKEN")
    print("    - CLOUDFLARE_ACCOUNT_ID\n")
    
    try:
        # Run examples
        # Uncomment the examples you want to run
        
        # example_1_aws_processing()
        # example_2_gcp_processing()
        # example_3_cloudflare_stream()
        # example_4_batch_cloud_processing()
        # example_5_cost_optimization()
        # example_6_distributed_processing()
        
        print("\n✅ Examples completed!")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")


if __name__ == "__main__":
    main()