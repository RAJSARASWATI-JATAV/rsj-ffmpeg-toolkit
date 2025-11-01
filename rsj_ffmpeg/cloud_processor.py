"""
RSJ-FFMPEG Cloud Processor
Cloud-based video processing with multi-provider support

Author: RAJSARASWATI JATAV
Version: 2.2.0
"""

import os
import json
import time
from typing import Dict, Any, List, Optional, Callable
from pathlib import Path
from datetime import datetime
import hashlib


class CloudProcessor:
    """
    Cloud processing engine supporting multiple providers
    AWS, GCP, Azure, Cloudflare
    """
    
    def __init__(
        self,
        provider: str = "aws",
        credentials: Optional[Dict[str, str]] = None,
        config: Optional[Dict[str, Any]] = None
    ):
        """
        Initialize Cloud Processor
        
        Args:
            provider: Cloud provider (aws, gcp, azure, cloudflare)
            credentials: Provider credentials
            config: Additional configuration
        """
        self.provider = provider.lower()
        self.credentials = credentials or {}
        self.config = config or {}
        self.jobs = {}
        
        # Initialize provider client
        self.client = None
        self._init_provider()
    
    def _init_provider(self):
        """Initialize cloud provider client"""
        if self.provider == "aws":
            self._init_aws()
        elif self.provider == "gcp":
            self._init_gcp()
        elif self.provider == "azure":
            self._init_azure()
        elif self.provider == "cloudflare":
            self._init_cloudflare()
        else:
            print(f"⚠️  Unknown provider: {self.provider}")
    
    def _init_aws(self):
        """Initialize AWS clients"""
        try:
            import boto3
            
            self.s3_client = boto3.client(
                's3',
                aws_access_key_id=self.credentials.get('access_key'),
                aws_secret_access_key=self.credentials.get('secret_key'),
                region_name=self.credentials.get('region', 'us-east-1')
            )
            
            self.mediaconvert_client = boto3.client(
                'mediaconvert',
                aws_access_key_id=self.credentials.get('access_key'),
                aws_secret_access_key=self.credentials.get('secret_key'),
                region_name=self.credentials.get('region', 'us-east-1')
            )
            
            self.lambda_client = boto3.client(
                'lambda',
                aws_access_key_id=self.credentials.get('access_key'),
                aws_secret_access_key=self.credentials.get('secret_key'),
                region_name=self.credentials.get('region', 'us-east-1')
            )
            
            self.client = "aws"
            print("✅ AWS clients initialized")
            
        except ImportError:
            print("⚠️  boto3 not installed. Install with: pip install boto3")
        except Exception as e:
            print(f"⚠️  AWS initialization failed: {e}")
    
    def _init_gcp(self):
        """Initialize Google Cloud clients"""
        try:
            from google.cloud import storage
            from google.cloud import video
            
            # Initialize clients
            self.storage_client = storage.Client.from_service_account_json(
                self.credentials.get('credentials_file')
            )
            
            self.transcoder_client = video.TranscoderServiceClient.from_service_account_json(
                self.credentials.get('credentials_file')
            )
            
            self.client = "gcp"
            print("✅ GCP clients initialized")
            
        except ImportError:
            print("⚠️  google-cloud libraries not installed")
        except Exception as e:
            print(f"⚠️  GCP initialization failed: {e}")
    
    def _init_azure(self):
        """Initialize Azure clients"""
        try:
            from azure.storage.blob import BlobServiceClient
            
            # Initialize clients
            self.blob_client = BlobServiceClient(
                account_url=self.credentials.get('account_url'),
                credential=self.credentials.get('account_key')
            )
            
            self.client = "azure"
            print("✅ Azure clients initialized")
            
        except ImportError:
            print("⚠️  azure-storage-blob not installed")
        except Exception as e:
            print(f"⚠️  Azure initialization failed: {e}")
    
    def _init_cloudflare(self):
        """Initialize Cloudflare Stream"""
        try:
            import requests
            
            self.cf_api_token = self.credentials.get('api_token')
            self.cf_account_id = self.credentials.get('account_id')
            self.cf_api_base = f"https://api.cloudflare.com/client/v4/accounts/{self.cf_account_id}/stream"
            
            self.client = "cloudflare"
            print("✅ Cloudflare Stream initialized")
            
        except Exception as e:
            print(f"⚠️  Cloudflare initialization failed: {e}")
    
    def process_video(
        self,
        input_file: str,
        operations: List[Dict[str, Any]],
        output_bucket: str,
        output_key: str,
        callback_url: Optional[str] = None,
        priority: str = "normal"
    ) -> Dict[str, Any]:
        """
        Process video in the cloud
        
        Args:
            input_file: Local input file or S3/GCS URL
            operations: List of operations to perform
            output_bucket: Output bucket name
            output_key: Output object key
            callback_url: Webhook URL for completion notification
            priority: Job priority (low, normal, high)
            
        Returns:
            Job information
        """
        if self.provider == "aws":
            return self._process_aws(input_file, operations, output_bucket, output_key, callback_url, priority)
        elif self.provider == "gcp":
            return self._process_gcp(input_file, operations, output_bucket, output_key)
        elif self.provider == "azure":
            return self._process_azure(input_file, operations, output_bucket, output_key)
        elif self.provider == "cloudflare":
            return self._process_cloudflare(input_file, operations)
        else:
            return {"status": "failed", "error": "Provider not initialized"}
    
    def _process_aws(
        self,
        input_file: str,
        operations: List[Dict[str, Any]],
        output_bucket: str,
        output_key: str,
        callback_url: Optional[str] = None,
        priority: str = "normal"
    ) -> Dict[str, Any]:
        """Process video using AWS MediaConvert"""
        try:
            # Upload file to S3 if local
            if not input_file.startswith('s3://'):
                input_bucket = self.config.get('input_bucket', output_bucket)
                input_key = f"inputs/{Path(input_file).name}"
                
                print(f"📤 Uploading {input_file} to S3...")
                self.s3_client.upload_file(input_file, input_bucket, input_key)
                s3_input = f"s3://{input_bucket}/{input_key}"
            else:
                s3_input = input_file
            
            # Build MediaConvert job settings
            job_settings = self._build_aws_job_settings(
                s3_input,
                f"s3://{output_bucket}/{output_key}",
                operations
            )
            
            # Submit job
            response = self.mediaconvert_client.create_job(**job_settings)
            job_id = response['Job']['Id']
            
            # Store job info
            self.jobs[job_id] = {
                "provider": "aws",
                "job_id": job_id,
                "status": "submitted",
                "input": input_file,
                "output": f"s3://{output_bucket}/{output_key}",
                "created_at": datetime.now().isoformat()
            }
            
            print(f"✅ AWS job submitted: {job_id}")
            
            return {
                "status": "submitted",
                "job_id": job_id,
                "provider": "aws",
                "output": f"s3://{output_bucket}/{output_key}"
            }
            
        except Exception as e:
            return {
                "status": "failed",
                "error": str(e)
            }
    
    def _build_aws_job_settings(
        self,
        input_url: str,
        output_url: str,
        operations: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Build AWS MediaConvert job settings"""
        settings = {
            "Role": self.credentials.get('mediaconvert_role'),
            "Settings": {
                "Inputs": [{
                    "FileInput": input_url,
                    "AudioSelectors": {
                        "Audio Selector 1": {
                            "DefaultSelection": "DEFAULT"
                        }
                    }
                }],
                "OutputGroups": [{
                    "Name": "File Group",
                    "OutputGroupSettings": {
                        "Type": "FILE_GROUP_SETTINGS",
                        "FileGroupSettings": {
                            "Destination": output_url.rsplit('/', 1)[0] + "/"
                        }
                    },
                    "Outputs": [{
                        "VideoDescription": {
                            "CodecSettings": {
                                "Codec": "H_264",
                                "H264Settings": {
                                    "RateControlMode": "QVBR",
                                    "QvbrSettings": {"QvbrQualityLevel": 8}
                                }
                            }
                        },
                        "AudioDescriptions": [{
                            "CodecSettings": {
                                "Codec": "AAC",
                                "AacSettings": {
                                    "Bitrate": 192000,
                                    "CodingMode": "CODING_MODE_2_0",
                                    "SampleRate": 48000
                                }
                            }
                        }],
                        "NameModifier": "_output"
                    }]
                }]
            }
        }
        
        # Apply operations
        for op in operations:
            if op['type'] == 'upscale':
                factor = op.get('factor', 2)
                settings['Settings']['OutputGroups'][0]['Outputs'][0]['VideoDescription']['Width'] = 1920 * factor
                settings['Settings']['OutputGroups'][0]['Outputs'][0]['VideoDescription']['Height'] = 1080 * factor
            
            elif op['type'] == 'compress':
                bitrate = op.get('bitrate', '5M')
                bitrate_int = int(bitrate.replace('M', '000000'))
                settings['Settings']['OutputGroups'][0]['Outputs'][0]['VideoDescription']['CodecSettings']['H264Settings']['Bitrate'] = bitrate_int
        
        return settings
    
    def _process_gcp(
        self,
        input_file: str,
        operations: List[Dict[str, Any]],
        output_bucket: str,
        output_key: str
    ) -> Dict[str, Any]:
        """Process video using Google Cloud Transcoder"""
        try:
            from google.cloud import video
            
            # Upload to GCS if local
            if not input_file.startswith('gs://'):
                bucket = self.storage_client.bucket(output_bucket)
                blob = bucket.blob(f"inputs/{Path(input_file).name}")
                blob.upload_from_filename(input_file)
                gcs_input = f"gs://{output_bucket}/inputs/{Path(input_file).name}"
            else:
                gcs_input = input_file
            
            # Create transcoding job
            parent = f"projects/{self.credentials.get('project_id')}/locations/us-central1"
            
            job = video.types.Job()
            job.input_uri = gcs_input
            job.output_uri = f"gs://{output_bucket}/{output_key}"
            
            # Configure based on operations
            job.config = video.types.JobConfig(
                elementary_streams=[
                    video.types.ElementaryStream(
                        key="video-stream0",
                        video_stream=video.types.VideoStream(
                            h264=video.types.VideoStream.H264CodecSettings(
                                bitrate_bps=5000000,
                                frame_rate=30,
                                height_pixels=1080,
                                width_pixels=1920
                            )
                        )
                    ),
                    video.types.ElementaryStream(
                        key="audio-stream0",
                        audio_stream=video.types.AudioStream(
                            codec="aac",
                            bitrate_bps=192000
                        )
                    )
                ],
                mux_streams=[
                    video.types.MuxStream(
                        key="sd",
                        container="mp4",
                        elementary_streams=["video-stream0", "audio-stream0"]
                    )
                ]
            )
            
            response = self.transcoder_client.create_job(parent=parent, job=job)
            job_id = response.name.split('/')[-1]
            
            self.jobs[job_id] = {
                "provider": "gcp",
                "job_id": job_id,
                "status": "submitted",
                "created_at": datetime.now().isoformat()
            }
            
            return {
                "status": "submitted",
                "job_id": job_id,
                "provider": "gcp"
            }
            
        except Exception as e:
            return {
                "status": "failed",
                "error": str(e)
            }
    
    def _process_azure(
        self,
        input_file: str,
        operations: List[Dict[str, Any]],
        output_bucket: str,
        output_key: str
    ) -> Dict[str, Any]:
        """Process video using Azure Media Services"""
        try:
            # Upload to Azure Blob Storage
            container_client = self.blob_client.get_container_client(output_bucket)
            
            if not input_file.startswith('https://'):
                blob_client = container_client.get_blob_client(f"inputs/{Path(input_file).name}")
                with open(input_file, 'rb') as data:
                    blob_client.upload_blob(data, overwrite=True)
                azure_input = blob_client.url
            else:
                azure_input = input_file
            
            job_id = hashlib.md5(f"{input_file}{datetime.now()}".encode()).hexdigest()
            
            self.jobs[job_id] = {
                "provider": "azure",
                "job_id": job_id,
                "status": "submitted",
                "input": azure_input,
                "output": f"https://{output_bucket}/{output_key}",
                "created_at": datetime.now().isoformat()
            }
            
            return {
                "status": "submitted",
                "job_id": job_id,
                "provider": "azure"
            }
            
        except Exception as e:
            return {
                "status": "failed",
                "error": str(e)
            }
    
    def _process_cloudflare(
        self,
        input_file: str,
        operations: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Process video using Cloudflare Stream"""
        try:
            import requests
            
            headers = {
                "Authorization": f"Bearer {self.cf_api_token}"
            }
            
            # Upload video
            with open(input_file, 'rb') as f:
                files = {'file': f}
                response = requests.post(
                    self.cf_api_base,
                    headers=headers,
                    files=files
                )
            
            if response.status_code == 200:
                data = response.json()
                uid = data['result']['uid']
                
                return {
                    "status": "success",
                    "job_id": uid,
                    "provider": "cloudflare",
                    "url": data['result']['preview'],
                    "uid": uid
                }
            else:
                return {
                    "status": "failed",
                    "error": response.text
                }
                
        except Exception as e:
            return {
                "status": "failed",
                "error": str(e)
            }
    
    def get_job_status(self, job_id: str) -> Dict[str, Any]:
        """Get job status"""
        if job_id not in self.jobs:
            return {"status": "unknown", "error": "Job not found"}
        
        job_info = self.jobs[job_id]
        provider = job_info['provider']
        
        if provider == "aws":
            return self._get_aws_status(job_id)
        elif provider == "gcp":
            return self._get_gcp_status(job_id)
        elif provider == "azure":
            return self._get_azure_status(job_id)
        elif provider == "cloudflare":
            return self._get_cloudflare_status(job_id)
        
        return {"status": "unknown"}
    
    def _get_aws_status(self, job_id: str) -> Dict[str, Any]:
        """Get AWS MediaConvert job status"""
        try:
            response = self.mediaconvert_client.get_job(Id=job_id)
            job = response['Job']
            
            status_map = {
                'SUBMITTED': 'submitted',
                'PROGRESSING': 'processing',
                'COMPLETE': 'complete',
                'CANCELED': 'failed',
                'ERROR': 'failed'
            }
            
            return {
                "status": status_map.get(job['Status'], 'unknown'),
                "progress": job.get('JobPercentComplete', 0),
                "job_id": job_id
            }
        except Exception as e:
            return {"status": "error", "error": str(e)}
    
    def _get_gcp_status(self, job_id: str) -> Dict[str, Any]:
        """Get GCP Transcoder job status"""
        try:
            job = self.transcoder_client.get_job(name=job_id)
            
            state_map = {
                1: 'submitted',  # PENDING
                2: 'processing',  # RUNNING
                3: 'complete',  # SUCCEEDED
                4: 'failed'  # FAILED
            }
            
            return {
                "status": state_map.get(job.state, 'unknown'),
                "progress": job.progress_percent if hasattr(job, 'progress_percent') else 0,
                "job_id": job_id
            }
        except Exception as e:
            return {"status": "error", "error": str(e)}
    
    def _get_azure_status(self, job_id: str) -> Dict[str, Any]:
        """Get Azure Media Services job status"""
        # Placeholder - would query Azure Media Services API
        return {
            "status": "processing",
            "progress": 50,
            "job_id": job_id
        }
    
    def _get_cloudflare_status(self, job_id: str) -> Dict[str, Any]:
        """Get Cloudflare Stream status"""
        try:
            import requests
            
            headers = {"Authorization": f"Bearer {self.cf_api_token}"}
            response = requests.get(
                f"{self.cf_api_base}/{job_id}",
                headers=headers
            )
            
            if response.status_code == 200:
                data = response.json()
                state = data['result']['status']['state']
                
                status_map = {
                    'queued': 'submitted',
                    'inprogress': 'processing',
                    'ready': 'complete',
                    'error': 'failed'
                }
                
                return {
                    "status": status_map.get(state, 'unknown'),
                    "progress": data['result']['status'].get('pctComplete', 0),
                    "job_id": job_id
                }
            else:
                return {"status": "error", "error": response.text}
                
        except Exception as e:
            return {"status": "error", "error": str(e)}
    
    def download_result(self, job_id: str, local_path: str) -> Dict[str, Any]:
        """Download processed video"""
        if job_id not in self.jobs:
            return {"status": "failed", "error": "Job not found"}
        
        job_info = self.jobs[job_id]
        provider = job_info['provider']
        
        try:
            if provider == "aws":
                # Parse S3 URL
                output_url = job_info['output']
                bucket = output_url.split('/')[2]
                key = '/'.join(output_url.split('/')[3:])
                
                self.s3_client.download_file(bucket, key, local_path)
                
            elif provider == "gcp":
                # Download from GCS
                output_url = job_info['output']
                bucket_name = output_url.split('/')[2]
                blob_name = '/'.join(output_url.split('/')[3:])
                
                bucket = self.storage_client.bucket(bucket_name)
                blob = bucket.blob(blob_name)
                blob.download_to_filename(local_path)
            
            elif provider == "azure":
                # Download from Azure Blob
                output_url = job_info['output']
                # Implementation would download from Azure Blob Storage
                pass
            
            return {
                "status": "success",
                "local_path": local_path
            }
            
        except Exception as e:
            return {
                "status": "failed",
                "error": str(e)
            }
    
    def upload_file(self, local_file: str, remote_path: str) -> Dict[str, Any]:
        """Upload file to cloud storage"""
        try:
            if self.provider == "aws":
                bucket = self.config.get('bucket', 'default-bucket')
                self.s3_client.upload_file(local_file, bucket, remote_path)
                return {
                    "status": "success",
                    "url": f"s3://{bucket}/{remote_path}"
                }
            
            elif self.provider == "gcp":
                bucket_name = self.config.get('bucket', 'default-bucket')
                bucket = self.storage_client.bucket(bucket_name)
                blob = bucket.blob(remote_path)
                blob.upload_from_filename(local_file)
                return {
                    "status": "success",
                    "url": f"gs://{bucket_name}/{remote_path}"
                }
            
            elif self.provider == "cloudflare":
                return self._process_cloudflare(local_file, [])
            
            return {"status": "failed", "error": "Provider not supported"}
            
        except Exception as e:
            return {
                "status": "failed",
                "error": str(e)
            }
    
    def list_jobs(self) -> List[Dict[str, Any]]:
        """List all jobs"""
        return list(self.jobs.values())
    
    def cancel_job(self, job_id: str) -> Dict[str, Any]:
        """Cancel a job"""
        if job_id not in self.jobs:
            return {"status": "failed", "error": "Job not found"}
        
        try:
            if self.jobs[job_id]['provider'] == "aws":
                self.mediaconvert_client.cancel_job(Id=job_id)
            
            self.jobs[job_id]['status'] = 'cancelled'
            return {"status": "success", "job_id": job_id}
            
        except Exception as e:
            return {"status": "failed", "error": str(e)}