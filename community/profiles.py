#!/usr/bin/env python3
"""
RSJ-FFMPEG User Profiles & Community
User authentication, profiles, and preferences sync

Author: RAJSARASWATI JATAV
Version: 2.1.0
"""

import os
import json
import hashlib
import time
from typing import Dict, List, Optional
from datetime import datetime, timedelta


class UserProfile:
    """User profile management"""
    
    def __init__(self, user_id: str, data: Dict):
        self.user_id = user_id
        self.username = data.get('username', '')
        self.email = data.get('email', '')
        self.created_at = data.get('created_at', datetime.now().isoformat())
        self.preferences = data.get('preferences', {})
        self.stats = data.get('stats', {})
        self.achievements = data.get('achievements', [])
    
    def to_dict(self) -> Dict:
        """Convert profile to dictionary"""
        return {
            'user_id': self.user_id,
            'username': self.username,
            'email': self.email,
            'created_at': self.created_at,
            'preferences': self.preferences,
            'stats': self.stats,
            'achievements': self.achievements
        }


class CommunityManager:
    """Community features and user management"""
    
    def __init__(self, config: Dict):
        self.config = config
        self.users_dir = config.get('users_dir', './users/')
        self.sessions_dir = config.get('sessions_dir', './sessions/')
        
        os.makedirs(self.users_dir, exist_ok=True)
        os.makedirs(self.sessions_dir, exist_ok=True)
        
        self.current_user = None
    
    def register_user(
        self,
        username: str,
        email: str,
        password: str
    ) -> Optional[str]:
        """
        Register new user
        
        Args:
            username: Username
            email: Email address
            password: Password
            
        Returns:
            User ID or None if failed
        """
        # Check if username exists
        if self._username_exists(username):
            print(f"❌ Username already exists: {username}")
            return None
        
        # Check if email exists
        if self._email_exists(email):
            print(f"❌ Email already registered: {email}")
            return None
        
        # Create user
        user_id = self._generate_user_id(username)
        password_hash = self._hash_password(password)
        
        user_data = {
            'user_id': user_id,
            'username': username,
            'email': email,
            'password_hash': password_hash,
            'created_at': datetime.now().isoformat(),
            'preferences': self._get_default_preferences(),
            'stats': {
                'videos_processed': 0,
                'total_processing_time': 0,
                'favorite_preset': None,
                'plugins_installed': 0
            },
            'achievements': []
        }
        
        # Save user
        user_file = os.path.join(self.users_dir, f"{user_id}.json")
        with open(user_file, 'w') as f:
            json.dump(user_data, f, indent=2)
        
        print(f"✅ User registered: {username}")
        return user_id
    
    def login(self, username: str, password: str) -> Optional[str]:
        """
        Login user
        
        Args:
            username: Username
            password: Password
            
        Returns:
            Session token or None if failed
        """
        user_data = self._get_user_by_username(username)
        
        if not user_data:
            print(f"❌ User not found: {username}")
            return None
        
        # Verify password
        password_hash = self._hash_password(password)
        if password_hash != user_data['password_hash']:
            print(f"❌ Invalid password")
            return None
        
        # Create session
        session_token = self._create_session(user_data['user_id'])
        
        # Load user profile
        self.current_user = UserProfile(user_data['user_id'], user_data)
        
        print(f"✅ Logged in: {username}")
        return session_token
    
    def logout(self, session_token: str) -> bool:
        """
        Logout user
        
        Args:
            session_token: Session token
            
        Returns:
            Success status
        """
        session_file = os.path.join(self.sessions_dir, f"{session_token}.json")
        
        if os.path.exists(session_file):
            os.remove(session_file)
        
        self.current_user = None
        print("✅ Logged out")
        return True
    
    def get_profile(self, user_id: str) -> Optional[UserProfile]:
        """
        Get user profile
        
        Args:
            user_id: User ID
            
        Returns:
            User profile or None
        """
        user_file = os.path.join(self.users_dir, f"{user_id}.json")
        
        if not os.path.exists(user_file):
            return None
        
        with open(user_file, 'r') as f:
            user_data = json.load(f)
        
        return UserProfile(user_id, user_data)
    
    def update_preferences(
        self,
        user_id: str,
        preferences: Dict
    ) -> bool:
        """
        Update user preferences
        
        Args:
            user_id: User ID
            preferences: Preferences dictionary
            
        Returns:
            Success status
        """
        user_file = os.path.join(self.users_dir, f"{user_id}.json")
        
        if not os.path.exists(user_file):
            return False
        
        with open(user_file, 'r') as f:
            user_data = json.load(f)
        
        user_data['preferences'].update(preferences)
        
        with open(user_file, 'w') as f:
            json.dump(user_data, f, indent=2)
        
        print("✅ Preferences updated")
        return True
    
    def sync_preferences(self, user_id: str) -> Dict:
        """
        Sync preferences across devices
        
        Args:
            user_id: User ID
            
        Returns:
            Synced preferences
        """
        profile = self.get_profile(user_id)
        
        if not profile:
            return {}
        
        print("🔄 Syncing preferences...")
        
        # In production, sync with cloud
        return profile.preferences
    
    def track_usage(
        self,
        user_id: str,
        operation: str,
        duration: float
    ) -> None:
        """
        Track user usage statistics
        
        Args:
            user_id: User ID
            operation: Operation performed
            duration: Processing duration
        """
        user_file = os.path.join(self.users_dir, f"{user_id}.json")
        
        if not os.path.exists(user_file):
            return
        
        with open(user_file, 'r') as f:
            user_data = json.load(f)
        
        user_data['stats']['videos_processed'] += 1
        user_data['stats']['total_processing_time'] += duration
        
        with open(user_file, 'w') as f:
            json.dump(user_data, f, indent=2)
    
    def award_achievement(
        self,
        user_id: str,
        achievement_id: str,
        achievement_name: str
    ) -> bool:
        """
        Award achievement to user
        
        Args:
            user_id: User ID
            achievement_id: Achievement identifier
            achievement_name: Achievement name
            
        Returns:
            Success status
        """
        user_file = os.path.join(self.users_dir, f"{user_id}.json")
        
        if not os.path.exists(user_file):
            return False
        
        with open(user_file, 'r') as f:
            user_data = json.load(f)
        
        # Check if already awarded
        if achievement_id in [a['id'] for a in user_data['achievements']]:
            return False
        
        achievement = {
            'id': achievement_id,
            'name': achievement_name,
            'awarded_at': datetime.now().isoformat()
        }
        
        user_data['achievements'].append(achievement)
        
        with open(user_file, 'w') as f:
            json.dump(user_data, f, indent=2)
        
        print(f"🏆 Achievement unlocked: {achievement_name}")
        return True
    
    def get_leaderboard(self, metric: str = 'videos_processed') -> List[Dict]:
        """
        Get community leaderboard
        
        Args:
            metric: Metric to rank by
            
        Returns:
            Leaderboard list
        """
        users = []
        
        for user_file in os.listdir(self.users_dir):
            if user_file.endswith('.json'):
                with open(os.path.join(self.users_dir, user_file), 'r') as f:
                    user_data = json.load(f)
                    users.append({
                        'username': user_data['username'],
                        'value': user_data['stats'].get(metric, 0)
                    })
        
        users.sort(key=lambda u: u['value'], reverse=True)
        return users[:10]
    
    def _username_exists(self, username: str) -> bool:
        """Check if username exists"""
        for user_file in os.listdir(self.users_dir):
            if user_file.endswith('.json'):
                with open(os.path.join(self.users_dir, user_file), 'r') as f:
                    user_data = json.load(f)
                    if user_data['username'] == username:
                        return True
        return False
    
    def _email_exists(self, email: str) -> bool:
        """Check if email exists"""
        for user_file in os.listdir(self.users_dir):
            if user_file.endswith('.json'):
                with open(os.path.join(self.users_dir, user_file), 'r') as f:
                    user_data = json.load(f)
                    if user_data['email'] == email:
                        return True
        return False
    
    def _get_user_by_username(self, username: str) -> Optional[Dict]:
        """Get user data by username"""
        for user_file in os.listdir(self.users_dir):
            if user_file.endswith('.json'):
                with open(os.path.join(self.users_dir, user_file), 'r') as f:
                    user_data = json.load(f)
                    if user_data['username'] == username:
                        return user_data
        return None
    
    def _generate_user_id(self, username: str) -> str:
        """Generate unique user ID"""
        return hashlib.sha256(
            f"{username}{time.time()}".encode()
        ).hexdigest()[:16]
    
    def _hash_password(self, password: str) -> str:
        """Hash password"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def _create_session(self, user_id: str) -> str:
        """Create user session"""
        session_token = hashlib.sha256(
            f"{user_id}{time.time()}".encode()
        ).hexdigest()
        
        session_data = {
            'user_id': user_id,
            'created_at': datetime.now().isoformat(),
            'expires_at': (datetime.now() + timedelta(days=30)).isoformat()
        }
        
        session_file = os.path.join(self.sessions_dir, f"{session_token}.json")
        with open(session_file, 'w') as f:
            json.dump(session_data, f, indent=2)
        
        return session_token
    
    def _get_default_preferences(self) -> Dict:
        """Get default user preferences"""
        return {
            'default_quality': 'high',
            'default_preset': 'cinematic',
            'enable_gpu': True,
            'enable_cache': True,
            'auto_watermark': False,
            'watermark_text': '',
            'theme': 'cyberpunk',
            'notifications': True
        }


# CLI Integration
if __name__ == '__main__':
    print("""
    ╔══════════════════════════════════════════════════════════════╗
    ║  RSJ-FFMPEG COMMUNITY & USER PROFILES                        ║
    ║  User Authentication, Profiles & Preferences Sync           ║
    ║  By RAJSARASWATI JATAV                                      ║
    ╚══════════════════════════════════════════════════════════════╝
    """)
    
    config = {}
    community = CommunityManager(config)
    
    print("\n📋 Available Commands:")
    print("  • register_user() - Register new user")
    print("  • login() - Login user")
    print("  • get_profile() - Get user profile")
    print("  • update_preferences() - Update preferences")
    print("  • sync_preferences() - Sync across devices")
    print("  • get_leaderboard() - View leaderboard")