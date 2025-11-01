#!/usr/bin/env python3
"""
RSJ-FFMPEG Intelligent Caching System
Smart caching for thumbnails, metadata, and processed files

Author: RAJSARASWATI JATAV
Version: 2.1.0
"""

import os
import json
import hashlib
import time
import shutil
from typing import Dict, List, Optional, Any
from pathlib import Path
from datetime import datetime, timedelta


class CacheManager:
    """Intelligent caching system for multimedia processing"""
    
    def __init__(self, config: Dict):
        self.config = config
        self.cache_dir = config.get('cache_dir', './cache/')
        self.max_cache_size = config.get('max_cache_size_gb', 10) * 1024 * 1024 * 1024
        self.cache_ttl_days = config.get('cache_ttl_days', 30)
        
        # Create cache directories
        self.thumbnail_cache = os.path.join(self.cache_dir, 'thumbnails')
        self.metadata_cache = os.path.join(self.cache_dir, 'metadata')
        self.processed_cache = os.path.join(self.cache_dir, 'processed')
        self.temp_cache = os.path.join(self.cache_dir, 'temp')
        
        for cache_path in [self.thumbnail_cache, self.metadata_cache, 
                          self.processed_cache, self.temp_cache]:
            os.makedirs(cache_path, exist_ok=True)
        
        # Cache index
        self.index_file = os.path.join(self.cache_dir, 'cache_index.json')
        self.index = self._load_index()
    
    def get_file_hash(self, file_path: str) -> str:
        """
        Generate hash for file
        
        Args:
            file_path: Path to file
            
        Returns:
            SHA256 hash
        """
        hasher = hashlib.sha256()
        
        # Hash file path and modification time
        hasher.update(file_path.encode())
        
        if os.path.exists(file_path):
            mtime = str(os.path.getmtime(file_path))
            hasher.update(mtime.encode())
        
        return hasher.hexdigest()
    
    def cache_thumbnail(
        self,
        video_file: str,
        thumbnail_data: bytes,
        timestamp: float = 0.0
    ) -> str:
        """
        Cache video thumbnail
        
        Args:
            video_file: Source video path
            thumbnail_data: Thumbnail image data
            timestamp: Thumbnail timestamp
            
        Returns:
            Cached thumbnail path
        """
        file_hash = self.get_file_hash(video_file)
        cache_key = f"{file_hash}_{timestamp}"
        cache_path = os.path.join(self.thumbnail_cache, f"{cache_key}.jpg")
        
        # Write thumbnail
        with open(cache_path, 'wb') as f:
            f.write(thumbnail_data)
        
        # Update index
        self._update_index('thumbnail', cache_key, {
            'source': video_file,
            'timestamp': timestamp,
            'path': cache_path,
            'size': len(thumbnail_data),
            'created': time.time()
        })
        
        print(f"✅ Thumbnail cached: {cache_key}")
        return cache_path
    
    def get_thumbnail(
        self,
        video_file: str,
        timestamp: float = 0.0
    ) -> Optional[str]:
        """
        Retrieve cached thumbnail
        
        Args:
            video_file: Source video path
            timestamp: Thumbnail timestamp
            
        Returns:
            Cached thumbnail path or None
        """
        file_hash = self.get_file_hash(video_file)
        cache_key = f"{file_hash}_{timestamp}"
        
        if cache_key in self.index.get('thumbnail', {}):
            cache_info = self.index['thumbnail'][cache_key]
            cache_path = cache_info['path']
            
            if os.path.exists(cache_path):
                # Check if cache is still valid
                if self._is_cache_valid(cache_info['created']):
                    print(f"✅ Thumbnail cache hit: {cache_key}")
                    return cache_path
                else:
                    # Remove expired cache
                    self._remove_cache_entry('thumbnail', cache_key)
        
        print(f"❌ Thumbnail cache miss: {cache_key}")
        return None
    
    def cache_metadata(
        self,
        video_file: str,
        metadata: Dict
    ) -> str:
        """
        Cache video metadata
        
        Args:
            video_file: Source video path
            metadata: Metadata dictionary
            
        Returns:
            Cached metadata path
        """
        file_hash = self.get_file_hash(video_file)
        cache_path = os.path.join(self.metadata_cache, f"{file_hash}.json")
        
        # Write metadata
        with open(cache_path, 'w') as f:
            json.dump(metadata, f, indent=2)
        
        # Update index
        self._update_index('metadata', file_hash, {
            'source': video_file,
            'path': cache_path,
            'size': os.path.getsize(cache_path),
            'created': time.time()
        })
        
        print(f"✅ Metadata cached: {file_hash}")
        return cache_path
    
    def get_metadata(self, video_file: str) -> Optional[Dict]:
        """
        Retrieve cached metadata
        
        Args:
            video_file: Source video path
            
        Returns:
            Cached metadata or None
        """
        file_hash = self.get_file_hash(video_file)
        
        if file_hash in self.index.get('metadata', {}):
            cache_info = self.index['metadata'][file_hash]
            cache_path = cache_info['path']
            
            if os.path.exists(cache_path):
                if self._is_cache_valid(cache_info['created']):
                    with open(cache_path, 'r') as f:
                        metadata = json.load(f)
                    print(f"✅ Metadata cache hit: {file_hash}")
                    return metadata
                else:
                    self._remove_cache_entry('metadata', file_hash)
        
        print(f"❌ Metadata cache miss: {file_hash}")
        return None
    
    def cache_processed_file(
        self,
        source_file: str,
        processed_file: str,
        operation: str,
        params: Dict
    ) -> str:
        """
        Cache processed file
        
        Args:
            source_file: Source file path
            processed_file: Processed file path
            operation: Operation name
            params: Operation parameters
            
        Returns:
            Cached file path
        """
        # Create cache key from source + operation + params
        cache_key_data = f"{source_file}_{operation}_{json.dumps(params, sort_keys=True)}"
        cache_key = hashlib.sha256(cache_key_data.encode()).hexdigest()
        
        file_ext = os.path.splitext(processed_file)[1]
        cache_path = os.path.join(self.processed_cache, f"{cache_key}{file_ext}")
        
        # Copy processed file to cache
        shutil.copy2(processed_file, cache_path)
        
        # Update index
        self._update_index('processed', cache_key, {
            'source': source_file,
            'operation': operation,
            'params': params,
            'path': cache_path,
            'size': os.path.getsize(cache_path),
            'created': time.time()
        })
        
        print(f"✅ Processed file cached: {cache_key}")
        return cache_path
    
    def get_processed_file(
        self,
        source_file: str,
        operation: str,
        params: Dict
    ) -> Optional[str]:
        """
        Retrieve cached processed file
        
        Args:
            source_file: Source file path
            operation: Operation name
            params: Operation parameters
            
        Returns:
            Cached file path or None
        """
        cache_key_data = f"{source_file}_{operation}_{json.dumps(params, sort_keys=True)}"
        cache_key = hashlib.sha256(cache_key_data.encode()).hexdigest()
        
        if cache_key in self.index.get('processed', {}):
            cache_info = self.index['processed'][cache_key]
            cache_path = cache_info['path']
            
            if os.path.exists(cache_path):
                if self._is_cache_valid(cache_info['created']):
                    print(f"✅ Processed file cache hit: {cache_key}")
                    return cache_path
                else:
                    self._remove_cache_entry('processed', cache_key)
        
        print(f"❌ Processed file cache miss: {cache_key}")
        return None
    
    def get_cache_stats(self) -> Dict:
        """
        Get cache statistics
        
        Returns:
            Cache statistics dictionary
        """
        stats = {
            'total_size': 0,
            'total_files': 0,
            'by_type': {}
        }
        
        for cache_type in ['thumbnail', 'metadata', 'processed']:
            type_stats = {
                'count': 0,
                'size': 0
            }
            
            if cache_type in self.index:
                type_stats['count'] = len(self.index[cache_type])
                
                for cache_info in self.index[cache_type].values():
                    type_stats['size'] += cache_info.get('size', 0)
            
            stats['by_type'][cache_type] = type_stats
            stats['total_size'] += type_stats['size']
            stats['total_files'] += type_stats['count']
        
        stats['total_size_mb'] = stats['total_size'] / (1024 * 1024)
        stats['max_size_gb'] = self.max_cache_size / (1024 * 1024 * 1024)
        stats['usage_percent'] = (stats['total_size'] / self.max_cache_size) * 100
        
        return stats
    
    def clean_cache(
        self,
        max_age_days: Optional[int] = None,
        force: bool = False
    ) -> Dict:
        """
        Clean expired cache entries
        
        Args:
            max_age_days: Maximum age in days (None = use default)
            force: Force clean all cache
            
        Returns:
            Cleanup report
        """
        print("🧹 Cleaning cache...")
        
        if max_age_days is None:
            max_age_days = self.cache_ttl_days
        
        cutoff_time = time.time() - (max_age_days * 24 * 60 * 60)
        
        report = {
            'removed_files': 0,
            'freed_space': 0,
            'by_type': {}
        }
        
        for cache_type in ['thumbnail', 'metadata', 'processed']:
            if cache_type not in self.index:
                continue
            
            type_report = {'count': 0, 'size': 0}
            to_remove = []
            
            for cache_key, cache_info in self.index[cache_type].items():
                should_remove = force or cache_info['created'] < cutoff_time
                
                if should_remove:
                    cache_path = cache_info['path']
                    if os.path.exists(cache_path):
                        size = os.path.getsize(cache_path)
                        os.remove(cache_path)
                        type_report['size'] += size
                    
                    to_remove.append(cache_key)
                    type_report['count'] += 1
            
            # Remove from index
            for cache_key in to_remove:
                del self.index[cache_type][cache_key]
            
            report['by_type'][cache_type] = type_report
            report['removed_files'] += type_report['count']
            report['freed_space'] += type_report['size']
        
        # Save updated index
        self._save_index()
        
        report['freed_space_mb'] = report['freed_space'] / (1024 * 1024)
        
        print(f"✅ Cache cleaned: {report['removed_files']} files, {report['freed_space_mb']:.2f} MB freed")
        return report
    
    def clear_all_cache(self) -> bool:
        """
        Clear all cache
        
        Returns:
            Success status
        """
        print("🗑️ Clearing all cache...")
        
        try:
            shutil.rmtree(self.cache_dir)
            os.makedirs(self.cache_dir, exist_ok=True)
            
            # Recreate cache directories
            for cache_path in [self.thumbnail_cache, self.metadata_cache,
                              self.processed_cache, self.temp_cache]:
                os.makedirs(cache_path, exist_ok=True)
            
            # Reset index
            self.index = {'thumbnail': {}, 'metadata': {}, 'processed': {}}
            self._save_index()
            
            print("✅ All cache cleared")
            return True
        except Exception as e:
            print(f"❌ Cache clear failed: {e}")
            return False
    
    def _load_index(self) -> Dict:
        """Load cache index"""
        if os.path.exists(self.index_file):
            try:
                with open(self.index_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        
        return {'thumbnail': {}, 'metadata': {}, 'processed': {}}
    
    def _save_index(self) -> None:
        """Save cache index"""
        with open(self.index_file, 'w') as f:
            json.dump(self.index, f, indent=2)
    
    def _update_index(
        self,
        cache_type: str,
        cache_key: str,
        cache_info: Dict
    ) -> None:
        """Update cache index"""
        if cache_type not in self.index:
            self.index[cache_type] = {}
        
        self.index[cache_type][cache_key] = cache_info
        self._save_index()
    
    def _remove_cache_entry(
        self,
        cache_type: str,
        cache_key: str
    ) -> None:
        """Remove cache entry"""
        if cache_type in self.index and cache_key in self.index[cache_type]:
            cache_info = self.index[cache_type][cache_key]
            cache_path = cache_info['path']
            
            if os.path.exists(cache_path):
                os.remove(cache_path)
            
            del self.index[cache_type][cache_key]
            self._save_index()
    
    def _is_cache_valid(self, created_time: float) -> bool:
        """Check if cache entry is still valid"""
        age_days = (time.time() - created_time) / (24 * 60 * 60)
        return age_days < self.cache_ttl_days


# CLI Integration
if __name__ == '__main__':
    print("""
    ╔══════════════════════════════════════════════════════════════╗
    ║  RSJ-FFMPEG INTELLIGENT CACHING SYSTEM                       ║
    ║  Smart Caching for Thumbnails, Metadata & Processed Files   ║
    ║  By RAJSARASWATI JATAV                                      ║
    ╚══════════════════════════════════════════════════════════════╝
    """)
    
    config = {}
    cache = CacheManager(config)
    
    # Display cache stats
    stats = cache.get_cache_stats()
    print(f"\n📊 Cache Statistics:")
    print(f"  Total Files: {stats['total_files']}")
    print(f"  Total Size: {stats['total_size_mb']:.2f} MB")
    print(f"  Usage: {stats['usage_percent']:.1f}%")
    print(f"\n  By Type:")
    for cache_type, type_stats in stats['by_type'].items():
        print(f"    {cache_type}: {type_stats['count']} files, {type_stats['size']/(1024*1024):.2f} MB")