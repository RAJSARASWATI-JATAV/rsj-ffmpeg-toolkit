#!/usr/bin/env python3
"""
RSJ-FFMPEG Advanced Analytics Dashboard v2
Real-time analytics, insights, and performance monitoring

Author: RAJSARASWATI JATAV
Version: 2.2.0
"""

from flask import Flask, render_template, jsonify, request
from flask_socketio import SocketIO, emit
from flask_cors import CORS
import os
import json
import time
import psutil
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from collections import defaultdict
import threading


app = Flask(__name__)
app.config['SECRET_KEY'] = 'rsj-ffmpeg-analytics-v2-2025'
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")


class AnalyticsEngine:
    """Advanced analytics and insights engine"""
    
    def __init__(self):
        self.jobs_history = []
        self.performance_metrics = []
        self.system_metrics = []
        self.ai_insights = []
        self.cost_tracking = []
        
        # Start background monitoring
        self.monitoring = True
        self.monitor_thread = threading.Thread(target=self._monitor_system)
        self.monitor_thread.daemon = True
        self.monitor_thread.start()
    
    def _monitor_system(self):
        """Background system monitoring"""
        while self.monitoring:
            try:
                metrics = {
                    "timestamp": datetime.now().isoformat(),
                    "cpu_percent": psutil.cpu_percent(interval=1),
                    "memory_percent": psutil.virtual_memory().percent,
                    "disk_usage": psutil.disk_usage('/').percent,
                    "network_io": psutil.net_io_counters()._asdict()
                }
                
                # Try to get GPU stats if available
                try:
                    import GPUtil
                    gpus = GPUtil.getGPUs()
                    if gpus:
                        metrics["gpu_percent"] = gpus[0].load * 100
                        metrics["gpu_memory"] = gpus[0].memoryUtil * 100
                except:
                    pass
                
                self.system_metrics.append(metrics)
                
                # Keep only last 1000 metrics
                if len(self.system_metrics) > 1000:
                    self.system_metrics = self.system_metrics[-1000:]
                
                # Emit to connected clients
                socketio.emit('system_metrics', metrics)
                
            except Exception as e:
                print(f"⚠️  Monitoring error: {e}")
            
            time.sleep(5)  # Update every 5 seconds
    
    def add_job(self, job: Dict[str, Any]):
        """Add job to history"""
        job['added_at'] = datetime.now().isoformat()
        self.jobs_history.append(job)
        
        # Keep only last 10000 jobs
        if len(self.jobs_history) > 10000:
            self.jobs_history = self.jobs_history[-10000:]
    
    def get_job_statistics(
        self,
        time_range: str = "24h"
    ) -> Dict[str, Any]:
        """Get job statistics for time range"""
        cutoff = self._get_cutoff_time(time_range)
        
        recent_jobs = [
            j for j in self.jobs_history
            if datetime.fromisoformat(j['added_at']) >= cutoff
        ]
        
        total = len(recent_jobs)
        completed = len([j for j in recent_jobs if j.get('status') == 'completed'])
        failed = len([j for j in recent_jobs if j.get('status') == 'failed'])
        processing = len([j for j in recent_jobs if j.get('status') == 'processing'])
        
        # Calculate average processing time
        processing_times = [
            j.get('processing_time', 0)
            for j in recent_jobs
            if j.get('status') == 'completed' and j.get('processing_time')
        ]
        avg_time = sum(processing_times) / len(processing_times) if processing_times else 0
        
        # Group by operation type
        operations = defaultdict(int)
        for job in recent_jobs:
            op_type = job.get('type', 'unknown')
            operations[op_type] += 1
        
        return {
            "total_jobs": total,
            "completed": completed,
            "failed": failed,
            "processing": processing,
            "success_rate": (completed / total * 100) if total > 0 else 0,
            "average_processing_time": avg_time,
            "operations": dict(operations),
            "time_range": time_range
        }
    
    def get_performance_insights(self) -> List[Dict[str, Any]]:
        """Generate performance insights"""
        insights = []
        
        # Analyze recent system metrics
        if len(self.system_metrics) > 10:
            recent = self.system_metrics[-100:]
            
            avg_cpu = sum(m['cpu_percent'] for m in recent) / len(recent)
            avg_memory = sum(m['memory_percent'] for m in recent) / len(recent)
            
            # High CPU usage
            if avg_cpu > 80:
                insights.append({
                    "type": "warning",
                    "category": "performance",
                    "message": f"High CPU usage detected ({avg_cpu:.1f}%)",
                    "recommendation": "Consider reducing parallel jobs or upgrading hardware",
                    "priority": "high"
                })
            
            # High memory usage
            if avg_memory > 85:
                insights.append({
                    "type": "warning",
                    "category": "performance",
                    "message": f"High memory usage detected ({avg_memory:.1f}%)",
                    "recommendation": "Close unnecessary applications or add more RAM",
                    "priority": "high"
                })
        
        # Analyze job success rate
        stats = self.get_job_statistics("24h")
        if stats['success_rate'] < 80 and stats['total_jobs'] > 10:
            insights.append({
                "type": "alert",
                "category": "reliability",
                "message": f"Low success rate ({stats['success_rate']:.1f}%)",
                "recommendation": "Check error logs and input file quality",
                "priority": "high"
            })
        
        # Analyze processing times
        if stats['average_processing_time'] > 300:  # 5 minutes
            insights.append({
                "type": "info",
                "category": "optimization",
                "message": "Long average processing time detected",
                "recommendation": "Consider using GPU acceleration or cloud processing",
                "priority": "medium"
            })
        
        return insights
    
    def get_cost_analysis(
        self,
        time_range: str = "30d"
    ) -> Dict[str, Any]:
        """Analyze processing costs"""
        cutoff = self._get_cutoff_time(time_range)
        
        recent_costs = [
            c for c in self.cost_tracking
            if datetime.fromisoformat(c['timestamp']) >= cutoff
        ]
        
        total_cost = sum(c.get('cost', 0) for c in recent_costs)
        
        # Group by provider
        by_provider = defaultdict(float)
        for cost in recent_costs:
            provider = cost.get('provider', 'local')
            by_provider[provider] += cost.get('cost', 0)
        
        # Group by operation
        by_operation = defaultdict(float)
        for cost in recent_costs:
            operation = cost.get('operation', 'unknown')
            by_operation[operation] += cost.get('cost', 0)
        
        return {
            "total_cost": total_cost,
            "by_provider": dict(by_provider),
            "by_operation": dict(by_operation),
            "time_range": time_range,
            "currency": "USD"
        }
    
    def get_trending_operations(
        self,
        time_range: str = "7d"
    ) -> List[Dict[str, Any]]:
        """Get trending operations"""
        cutoff = self._get_cutoff_time(time_range)
        
        recent_jobs = [
            j for j in self.jobs_history
            if datetime.fromisoformat(j['added_at']) >= cutoff
        ]
        
        operations = defaultdict(int)
        for job in recent_jobs:
            op_type = job.get('type', 'unknown')
            operations[op_type] += 1
        
        # Sort by count
        trending = [
            {"operation": op, "count": count}
            for op, count in sorted(
                operations.items(),
                key=lambda x: x[1],
                reverse=True
            )
        ]
        
        return trending[:10]  # Top 10
    
    def _get_cutoff_time(self, time_range: str) -> datetime:
        """Get cutoff datetime for time range"""
        now = datetime.now()
        
        if time_range == "1h":
            return now - timedelta(hours=1)
        elif time_range == "24h":
            return now - timedelta(hours=24)
        elif time_range == "7d":
            return now - timedelta(days=7)
        elif time_range == "30d":
            return now - timedelta(days=30)
        else:
            return now - timedelta(hours=24)
    
    def export_analytics(
        self,
        format: str = "json",
        time_range: str = "30d"
    ) -> str:
        """Export analytics data"""
        data = {
            "exported_at": datetime.now().isoformat(),
            "time_range": time_range,
            "job_statistics": self.get_job_statistics(time_range),
            "performance_insights": self.get_performance_insights(),
            "cost_analysis": self.get_cost_analysis(time_range),
            "trending_operations": self.get_trending_operations(time_range)
        }
        
        if format == "json":
            return json.dumps(data, indent=2)
        else:
            # Could add CSV, PDF export
            return json.dumps(data, indent=2)


# Global analytics engine
analytics = AnalyticsEngine()


# API Routes
@app.route('/')
def index():
    """Analytics dashboard home"""
    return render_template('analytics_v2.html')


@app.route('/api/v2/analytics/stats')
def get_stats():
    """Get current statistics"""
    time_range = request.args.get('range', '24h')
    return jsonify(analytics.get_job_statistics(time_range))


@app.route('/api/v2/analytics/insights')
def get_insights():
    """Get performance insights"""
    return jsonify(analytics.get_performance_insights())


@app.route('/api/v2/analytics/costs')
def get_costs():
    """Get cost analysis"""
    time_range = request.args.get('range', '30d')
    return jsonify(analytics.get_cost_analysis(time_range))


@app.route('/api/v2/analytics/trending')
def get_trending():
    """Get trending operations"""
    time_range = request.args.get('range', '7d')
    return jsonify(analytics.get_trending_operations(time_range))


@app.route('/api/v2/analytics/system')
def get_system_metrics():
    """Get current system metrics"""
    if analytics.system_metrics:
        return jsonify(analytics.system_metrics[-1])
    return jsonify({})


@app.route('/api/v2/analytics/export')
def export_analytics():
    """Export analytics data"""
    format = request.args.get('format', 'json')
    time_range = request.args.get('range', '30d')
    
    data = analytics.export_analytics(format, time_range)
    
    return data, 200, {
        'Content-Type': 'application/json',
        'Content-Disposition': f'attachment; filename=analytics_{time_range}.json'
    }


@app.route('/api/v2/analytics/jobs', methods=['POST'])
def add_job():
    """Add job to analytics"""
    job_data = request.json
    analytics.add_job(job_data)
    return jsonify({"status": "success"})


# WebSocket Events
@socketio.on('connect')
def handle_connect():
    """Handle client connection"""
    print('📊 Analytics client connected')
    emit('connected', {'message': 'Connected to analytics'})


@socketio.on('disconnect')
def handle_disconnect():
    """Handle client disconnection"""
    print('📊 Analytics client disconnected')


@socketio.on('request_update')
def handle_update_request():
    """Handle update request"""
    emit('stats_update', analytics.get_job_statistics())
    emit('insights_update', analytics.get_performance_insights())


if __name__ == '__main__':
    print("🚀 Starting RSJ-FFMPEG Analytics Dashboard v2...")
    print("📊 Dashboard: http://localhost:5001")
    socketio.run(app, host='0.0.0.0', port=5001, debug=True)