#!/usr/bin/env python3
"""
RSJ-FFMPEG Web Dashboard
Real-time monitoring and control panel

Author: RAJSARASWATI JATAV
Version: 2.1.0
"""

from flask import Flask, render_template, jsonify, request, send_from_directory
from flask_socketio import SocketIO, emit
import os
import json
import time
from datetime import datetime
from typing import Dict, List
import threading

app = Flask(__name__)
app.config['SECRET_KEY'] = 'rsj-ffmpeg-secret-key-2025'
socketio = SocketIO(app, cors_allowed_origins="*")

# Global state
dashboard_state = {
    'active_jobs': [],
    'completed_jobs': [],
    'failed_jobs': [],
    'system_stats': {
        'cpu_usage': 0,
        'memory_usage': 0,
        'gpu_usage': 0,
        'disk_usage': 0
    },
    'nodes': [],
    'cache_stats': {},
    'performance_metrics': []
}


@app.route('/')
def index():
    """Main dashboard page"""
    return render_template('dashboard.html')


@app.route('/api/stats')
def get_stats():
    """Get current system statistics"""
    return jsonify(dashboard_state)


@app.route('/api/jobs')
def get_jobs():
    """Get all jobs"""
    return jsonify({
        'active': dashboard_state['active_jobs'],
        'completed': dashboard_state['completed_jobs'],
        'failed': dashboard_state['failed_jobs']
    })


@app.route('/api/jobs/<job_id>')
def get_job(job_id):
    """Get specific job details"""
    for job in dashboard_state['active_jobs'] + dashboard_state['completed_jobs']:
        if job['id'] == job_id:
            return jsonify(job)
    return jsonify({'error': 'Job not found'}), 404


@app.route('/api/jobs', methods=['POST'])
def create_job():
    """Create new processing job"""
    data = request.json
    
    job = {
        'id': f"job_{int(time.time())}",
        'type': data.get('type', 'convert'),
        'input_file': data.get('input_file'),
        'output_file': data.get('output_file'),
        'params': data.get('params', {}),
        'status': 'queued',
        'progress': 0,
        'created_at': datetime.now().isoformat(),
        'started_at': None,
        'completed_at': None
    }
    
    dashboard_state['active_jobs'].append(job)
    
    # Emit socket event
    socketio.emit('job_created', job)
    
    return jsonify(job), 201


@app.route('/api/jobs/<job_id>/cancel', methods=['POST'])
def cancel_job(job_id):
    """Cancel a job"""
    for job in dashboard_state['active_jobs']:
        if job['id'] == job_id:
            job['status'] = 'cancelled'
            dashboard_state['active_jobs'].remove(job)
            dashboard_state['failed_jobs'].append(job)
            
            socketio.emit('job_cancelled', job)
            return jsonify({'message': 'Job cancelled'})
    
    return jsonify({'error': 'Job not found'}), 404


@app.route('/api/nodes')
def get_nodes():
    """Get cluster nodes"""
    return jsonify(dashboard_state['nodes'])


@app.route('/api/cache')
def get_cache_stats():
    """Get cache statistics"""
    return jsonify(dashboard_state['cache_stats'])


@app.route('/api/cache/clear', methods=['POST'])
def clear_cache():
    """Clear cache"""
    # Clear cache logic here
    socketio.emit('cache_cleared', {'timestamp': datetime.now().isoformat()})
    return jsonify({'message': 'Cache cleared'})


@app.route('/api/performance')
def get_performance():
    """Get performance metrics"""
    return jsonify(dashboard_state['performance_metrics'])


@socketio.on('connect')
def handle_connect():
    """Handle client connection"""
    emit('connected', {'message': 'Connected to RSJ-FFMPEG Dashboard'})


@socketio.on('disconnect')
def handle_disconnect():
    """Handle client disconnection"""
    print('Client disconnected')


@socketio.on('request_update')
def handle_update_request():
    """Handle update request from client"""
    emit('stats_update', dashboard_state)


def update_system_stats():
    """Background thread to update system statistics"""
    while True:
        try:
            import psutil
            
            dashboard_state['system_stats'] = {
                'cpu_usage': psutil.cpu_percent(interval=1),
                'memory_usage': psutil.virtual_memory().percent,
                'disk_usage': psutil.disk_usage('/').percent,
                'gpu_usage': 0  # Would get from GPU monitoring
            }
            
            # Emit to all connected clients
            socketio.emit('stats_update', dashboard_state['system_stats'])
            
        except Exception as e:
            print(f"Error updating stats: {e}")
        
        time.sleep(2)


def simulate_job_progress():
    """Simulate job progress for demo"""
    while True:
        for job in dashboard_state['active_jobs']:
            if job['status'] == 'processing':
                job['progress'] = min(job['progress'] + 5, 100)
                
                if job['progress'] >= 100:
                    job['status'] = 'completed'
                    job['completed_at'] = datetime.now().isoformat()
                    dashboard_state['active_jobs'].remove(job)
                    dashboard_state['completed_jobs'].append(job)
                    
                    socketio.emit('job_completed', job)
                else:
                    socketio.emit('job_progress', job)
        
        time.sleep(1)


if __name__ == '__main__':
    print("""
    ╔══════════════════════════════════════════════════════════════╗
    ║  RSJ-FFMPEG WEB DASHBOARD                                    ║
    ║  Real-time Monitoring & Control Panel                       ║
    ║  By RAJSARASWATI JATAV                                      ║
    ╚══════════════════════════════════════════════════════════════╝
    """)
    
    # Start background threads
    stats_thread = threading.Thread(target=update_system_stats, daemon=True)
    stats_thread.start()
    
    progress_thread = threading.Thread(target=simulate_job_progress, daemon=True)
    progress_thread.start()
    
    print("\n🌐 Dashboard starting on http://localhost:5000")
    print("📊 Real-time monitoring enabled")
    print("🔄 WebSocket connection active\n")
    
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)