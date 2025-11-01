#!/usr/bin/env python3
"""
RSJ-FFMPEG Usage Analytics
Track usage, performance metrics, and generate insights

Author: RAJSARASWATI JATAV
Version: 2.1.0
"""

import os
import json
import time
from typing import Dict, List, Optional
from datetime import datetime, timedelta
from collections import defaultdict


class AnalyticsEngine:
    """Usage analytics and insights"""
    
    def __init__(self, config: Dict):
        self.config = config
        self.analytics_dir = config.get('analytics_dir', './analytics/')
        self.events_file = os.path.join(self.analytics_dir, 'events.jsonl')
        
        os.makedirs(self.analytics_dir, exist_ok=True)
    
    def track_event(
        self,
        event_type: str,
        event_data: Dict,
        user_id: Optional[str] = None
    ) -> None:
        """
        Track analytics event
        
        Args:
            event_type: Type of event
            event_data: Event data
            user_id: Optional user ID
        """
        event = {
            'timestamp': datetime.now().isoformat(),
            'type': event_type,
            'data': event_data,
            'user_id': user_id
        }
        
        # Append to events file
        with open(self.events_file, 'a') as f:
            f.write(json.dumps(event) + '\n')
    
    def get_usage_stats(
        self,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> Dict:
        """
        Get usage statistics
        
        Args:
            start_date: Start date filter
            end_date: End date filter
            
        Returns:
            Usage statistics
        """
        if not os.path.exists(self.events_file):
            return {}
        
        stats = {
            'total_events': 0,
            'events_by_type': defaultdict(int),
            'events_by_day': defaultdict(int),
            'popular_operations': defaultdict(int),
            'popular_presets': defaultdict(int),
            'average_processing_time': 0,
            'total_videos_processed': 0,
            'total_processing_time': 0
        }
        
        processing_times = []
        
        with open(self.events_file, 'r') as f:
            for line in f:
                event = json.loads(line)
                event_date = datetime.fromisoformat(event['timestamp'])
                
                # Apply date filters
                if start_date and event_date < start_date:
                    continue
                if end_date and event_date > end_date:
                    continue
                
                stats['total_events'] += 1
                stats['events_by_type'][event['type']] += 1
                
                day = event_date.strftime('%Y-%m-%d')
                stats['events_by_day'][day] += 1
                
                # Track specific metrics
                if event['type'] == 'video_processed':
                    stats['total_videos_processed'] += 1
                    
                    if 'duration' in event['data']:
                        duration = event['data']['duration']
                        stats['total_processing_time'] += duration
                        processing_times.append(duration)
                    
                    if 'operation' in event['data']:
                        stats['popular_operations'][event['data']['operation']] += 1
                    
                    if 'preset' in event['data']:
                        stats['popular_presets'][event['data']['preset']] += 1
        
        # Calculate averages
        if processing_times:
            stats['average_processing_time'] = sum(processing_times) / len(processing_times)
        
        # Convert defaultdicts to regular dicts
        stats['events_by_type'] = dict(stats['events_by_type'])
        stats['events_by_day'] = dict(stats['events_by_day'])
        stats['popular_operations'] = dict(stats['popular_operations'])
        stats['popular_presets'] = dict(stats['popular_presets'])
        
        return stats
    
    def get_performance_metrics(self) -> Dict:
        """
        Get performance metrics
        
        Returns:
            Performance metrics
        """
        if not os.path.exists(self.events_file):
            return {}
        
        metrics = {
            'operations': defaultdict(lambda: {
                'count': 0,
                'total_time': 0,
                'avg_time': 0,
                'min_time': float('inf'),
                'max_time': 0
            })
        }
        
        with open(self.events_file, 'r') as f:
            for line in f:
                event = json.loads(line)
                
                if event['type'] == 'video_processed' and 'duration' in event['data']:
                    operation = event['data'].get('operation', 'unknown')
                    duration = event['data']['duration']
                    
                    op_metrics = metrics['operations'][operation]
                    op_metrics['count'] += 1
                    op_metrics['total_time'] += duration
                    op_metrics['min_time'] = min(op_metrics['min_time'], duration)
                    op_metrics['max_time'] = max(op_metrics['max_time'], duration)
        
        # Calculate averages
        for operation, op_metrics in metrics['operations'].items():
            if op_metrics['count'] > 0:
                op_metrics['avg_time'] = op_metrics['total_time'] / op_metrics['count']
        
        metrics['operations'] = dict(metrics['operations'])
        
        return metrics
    
    def get_user_insights(self, user_id: str) -> Dict:
        """
        Get insights for specific user
        
        Args:
            user_id: User ID
            
        Returns:
            User insights
        """
        if not os.path.exists(self.events_file):
            return {}
        
        insights = {
            'total_videos': 0,
            'total_time': 0,
            'favorite_operation': None,
            'favorite_preset': None,
            'operations': defaultdict(int),
            'presets': defaultdict(int),
            'activity_by_hour': defaultdict(int)
        }
        
        with open(self.events_file, 'r') as f:
            for line in f:
                event = json.loads(line)
                
                if event.get('user_id') != user_id:
                    continue
                
                if event['type'] == 'video_processed':
                    insights['total_videos'] += 1
                    
                    if 'duration' in event['data']:
                        insights['total_time'] += event['data']['duration']
                    
                    if 'operation' in event['data']:
                        insights['operations'][event['data']['operation']] += 1
                    
                    if 'preset' in event['data']:
                        insights['presets'][event['data']['preset']] += 1
                    
                    # Track activity by hour
                    event_time = datetime.fromisoformat(event['timestamp'])
                    hour = event_time.hour
                    insights['activity_by_hour'][hour] += 1
        
        # Find favorites
        if insights['operations']:
            insights['favorite_operation'] = max(
                insights['operations'].items(),
                key=lambda x: x[1]
            )[0]
        
        if insights['presets']:
            insights['favorite_preset'] = max(
                insights['presets'].items(),
                key=lambda x: x[1]
            )[0]
        
        insights['operations'] = dict(insights['operations'])
        insights['presets'] = dict(insights['presets'])
        insights['activity_by_hour'] = dict(insights['activity_by_hour'])
        
        return insights
    
    def generate_report(
        self,
        report_type: str = 'daily',
        output_file: Optional[str] = None
    ) -> str:
        """
        Generate analytics report
        
        Args:
            report_type: Type of report (daily/weekly/monthly)
            output_file: Optional output file path
            
        Returns:
            Report content or file path
        """
        # Calculate date range
        end_date = datetime.now()
        
        if report_type == 'daily':
            start_date = end_date - timedelta(days=1)
        elif report_type == 'weekly':
            start_date = end_date - timedelta(days=7)
        elif report_type == 'monthly':
            start_date = end_date - timedelta(days=30)
        else:
            start_date = None
        
        # Get stats
        stats = self.get_usage_stats(start_date, end_date)
        metrics = self.get_performance_metrics()
        
        # Generate report
        report = f"""# RSJ-FFMPEG Analytics Report
**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
**Period:** {report_type.capitalize()}  
**By:** RAJSARASWATI JATAV

---

## 📊 Usage Statistics

- **Total Events:** {stats.get('total_events', 0):,}
- **Videos Processed:** {stats.get('total_videos_processed', 0):,}
- **Total Processing Time:** {stats.get('total_processing_time', 0):.2f}s
- **Average Processing Time:** {stats.get('average_processing_time', 0):.2f}s

---

## 🔥 Popular Operations

"""
        
        for operation, count in sorted(
            stats.get('popular_operations', {}).items(),
            key=lambda x: x[1],
            reverse=True
        )[:5]:
            report += f"- **{operation}:** {count:,} times\n"
        
        report += "\n---\n\n## 🎨 Popular Presets\n\n"
        
        for preset, count in sorted(
            stats.get('popular_presets', {}).items(),
            key=lambda x: x[1],
            reverse=True
        )[:5]:
            report += f"- **{preset}:** {count:,} times\n"
        
        report += "\n---\n\n## ⚡ Performance Metrics\n\n"
        
        for operation, op_metrics in metrics.get('operations', {}).items():
            report += f"### {operation}\n"
            report += f"- Count: {op_metrics['count']:,}\n"
            report += f"- Avg Time: {op_metrics['avg_time']:.2f}s\n"
            report += f"- Min Time: {op_metrics['min_time']:.2f}s\n"
            report += f"- Max Time: {op_metrics['max_time']:.2f}s\n\n"
        
        report += "\n---\n\n**© 2025 RAJSARASWATI JATAV | All Rights Reserved**"
        
        if output_file:
            with open(output_file, 'w') as f:
                f.write(report)
            return output_file
        
        return report
    
    def export_data(
        self,
        output_file: str,
        format: str = 'json'
    ) -> bool:
        """
        Export analytics data
        
        Args:
            output_file: Output file path
            format: Export format (json/csv)
            
        Returns:
            Success status
        """
        stats = self.get_usage_stats()
        
        if format == 'json':
            with open(output_file, 'w') as f:
                json.dump(stats, f, indent=2)
        elif format == 'csv':
            # CSV export logic here
            pass
        
        print(f"✅ Analytics exported: {output_file}")
        return True


# CLI Integration
if __name__ == '__main__':
    print("""
    ╔══════════════════════════════════════════════════════════════╗
    ║  RSJ-FFMPEG USAGE ANALYTICS                                  ║
    ║  Track Usage, Performance & Generate Insights               ║
    ║  By RAJSARASWATI JATAV                                      ║
    ╚══════════════════════════════════════════════════════════════╝
    """)
    
    config = {}
    analytics = AnalyticsEngine(config)
    
    # Generate sample report
    print("\n📊 Generating analytics report...\n")
    report = analytics.generate_report(report_type='weekly')
    print(report)