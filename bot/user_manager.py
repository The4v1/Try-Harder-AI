"""
User Manager
============

Manages user data, progress tracking, and session persistence.

Features:
- User profile management
- Assessment results storage
- Roadmap persistence
- Progress tracking (machines, hours, milestones)
- User preferences
- JSON-based storage
- Statistics collection
- Data export/import
- Backup and restore
"""

import json
import logging
import os
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional, List

# Setup logging
logger = logging.getLogger(__name__)


class UserManager:
    """Manages user data and progress tracking with JSON persistence."""
    
    def __init__(self, storage_path: Optional[str] = None):
        """
        Initialize user manager.
        
        Args:
            storage_path: Path to JSON storage file (optional)
        """
        if storage_path:
            self.storage_path = Path(storage_path)
        else:
            # Default path
            data_dir = Path(__file__).parent.parent / 'data'
            data_dir.mkdir(parents=True, exist_ok=True)
            self.storage_path = data_dir / 'user_data.json'
        
        self.users: Dict[str, Dict[str, Any]] = {}
        
        # Ensure parent directory exists
        self.storage_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Load existing data
        self._load_data()
        
        logger.info(f"👥 User Manager initialized with {len(self.users)} users")
    
    def _load_data(self):
        """Load user data from JSON file."""
        try:
            if self.storage_path.exists():
                with open(self.storage_path, 'r', encoding='utf-8') as f:
                    self.users = json.load(f)
                logger.info(f"✅ Loaded data for {len(self.users)} users")
            else:
                logger.info("📝 No existing user data found, starting fresh")
                self.users = {}
                self._save_data()  # Create empty file
        except json.JSONDecodeError as e:
            logger.error(f"❌ Error parsing user data JSON: {e}")
            logger.warning("⚠️ Creating backup and starting with empty data")
            self._backup_corrupted_file()
            self.users = {}
        except Exception as e:
            logger.error(f"❌ Error loading user data: {e}")
            self.users = {}
    
    def _backup_corrupted_file(self):
        """Backup corrupted file before overwriting."""
        try:
            if self.storage_path.exists():
                backup_path = self.storage_path.with_suffix('.json.corrupted')
                self.storage_path.rename(backup_path)
                logger.info(f"💾 Corrupted file backed up to: {backup_path}")
        except Exception as e:
            logger.error(f"❌ Error backing up corrupted file: {e}")
    
    def _save_data(self):
        """Save user data to JSON file with automatic backup."""
        try:
            # Create backup before saving (daily backups with 7-day retention)
            self._create_backup()
            
            with open(self.storage_path, 'w', encoding='utf-8') as f:
                json.dump(self.users, f, indent=2, ensure_ascii=False)
            
            logger.debug(f"💾 Saved data for {len(self.users)} users")
        except Exception as e:
            logger.error(f"❌ Error saving user data: {e}")
    
    def _create_backup(self):
        """Create daily backup of user data and cleanup old backups."""
        try:
            if not os.path.exists(self.storage_path):
                return  # No file to backup yet
            
            # Get today's date for backup filename
            today = datetime.now().strftime("%Y-%m-%d")
            backup_filename = f"user_data.backup.{today}.json"
            backup_path = Path(self.storage_path).parent / backup_filename
            
            # Only create one backup per day (skip if today's backup exists)
            if backup_path.exists():
                return
            
            # Create backup
            import shutil
            shutil.copy2(self.storage_path, backup_path)
            logger.info(f"📦 Created backup: {backup_filename}")
            
            # Cleanup old backups (keep last 7 days)
            self._cleanup_old_backups()
        except Exception as e:
            logger.warning(f"⚠️ Failed to create backup: {e}")
    
    def _cleanup_old_backups(self):
        """Remove backups older than 7 days."""
        try:
            backup_dir = Path(self.storage_path).parent
            backup_pattern = "user_data.backup.*.json"
            
            from datetime import timedelta
            cutoff_date = datetime.now() - timedelta(days=7)
            
            # Find all backup files
            for backup_file in backup_dir.glob(backup_pattern):
                try:
                    # Extract date from filename
                    date_str = backup_file.stem.split('.')[-1]  # e.g., "2026-02-16"
                    backup_date = datetime.strptime(date_str, "%Y-%m-%d")
                    
                    # Delete if older than 7 days
                    if backup_date < cutoff_date:
                        backup_file.unlink()
                        logger.debug(f"🗑️ Deleted old backup: {backup_file.name}")
                except Exception as e:
                    logger.warning(f"⚠️ Failed to process backup file {backup_file.name}: {e}")
        except Exception as e:
            logger.warning(f"⚠️ Failed to cleanup old backups: {e}")
    
    def get_user_data(self, user_id: str) -> Optional[Dict[str, Any]]:
        """
        Get all data for a user.
        
        Args:
            user_id: Discord user ID
            
        Returns:
            User data dictionary or None
        """
        return self.users.get(str(user_id))
    
    def create_user(self, user_id: str, username: Optional[str] = None) -> Dict[str, Any]:
        """
        Create a new user profile.
        
        Args:
            user_id: Discord user ID
            username: Discord username (optional)
            
        Returns:
            Created user data
        """
        user_id = str(user_id)
        
        if user_id in self.users:
            logger.warning(f"⚠️ User {user_id} already exists")
            return self.users[user_id]
        
        user_data = {
            'user_id': user_id,
            'username': username,
            'created_at': datetime.now().isoformat(),
            'last_active': datetime.now().isoformat(),
            'assessment_results': None,
            'roadmap': None,
            'progress': {
                'machines_completed': 0,
                'hours_studied': 0,
                'current_phase': 1,
                'milestones_completed': []
            },
            'preferences': {
                'study_hours_per_week': 15,
                'notifications_enabled': True,
                'preferred_model': 'gemini-1.5-flash'
            },
            'history': {
                'assessments': [],
                'roadmaps_generated': []
            }
        }
        
        self.users[user_id] = user_data
        self._save_data()
        
        logger.info(f"✅ Created user profile: {user_id}")
        return user_data
    
    def update_last_active(self, user_id: str):
        """
        Update user's last active timestamp.
        
        Args:
            user_id: Discord user ID
        """
        user_id = str(user_id)
        
        if user_id not in self.users:
            self.create_user(user_id)
        
        self.users[user_id]['last_active'] = datetime.now().isoformat()
        self._save_data()
    
    def save_assessment_results(self, user_id: str, results: Dict[str, Any]):
        """
        Save assessment results for a user.
        
        Args:
            user_id: Discord user ID
            results: Assessment results dictionary
        """
        user_id = str(user_id)
        
        if user_id not in self.users:
            self.create_user(user_id)
        
        # Add timestamp
        results['saved_at'] = datetime.now().isoformat()
        
        # Save current results
        self.users[user_id]['assessment_results'] = results
        
        # Add to history
        if 'history' not in self.users[user_id]:
            self.users[user_id]['history'] = {'assessments': [], 'roadmaps_generated': []}
        
        self.users[user_id]['history']['assessments'].append({
            'certification': results.get('certification'),
            'score': results.get('score_percentage'),
            'skill_level': results.get('skill_level'),
            'timestamp': results['saved_at']
        })
        
        # Update last active
        self.users[user_id]['last_active'] = datetime.now().isoformat()
        
        self._save_data()
        
        logger.info(f"✅ Saved assessment results for user {user_id}")
        
        # Update progress based on assessment answers
        self._update_progress_from_assessment(user_id, results)
        
    def _update_progress_from_assessment(self, user_id: str, results: Dict[str, Any]):
        """
        Update user progress based on assessment answers.
        
        Args:
            user_id: Discord user ID
            results: Assessment results dictionary
        """
        try:
            answers = results.get('answers', [])
            machines_count = 0
            
            for answer in answers:
                question_text = answer.get('question', '').lower()
                # Check for machine count related questions
                if 'machines' in question_text and ('rooted' in question_text or 'completed' in question_text):
                    selected_option = answer.get('answer', '')
                    # Parse the number (e.g., "10-20 machines", "30+ machines")
                    # simple heuristic: find first number sequence
                    import re
                    numbers = re.findall(r'\d+', selected_option)
                    if numbers:
                        # Take the first number found (usually the lower bound or the count)
                        # e.g., "30+" -> 30, "10-20" -> 10
                        extracted_count = int(numbers[0])
                        if extracted_count > machines_count:
                            machines_count = extracted_count
                            
            # Update user progress if we found a valid count
            if machines_count > 0:
                self.update_progress(user_id, machines_completed=machines_count)
                logger.info(f"✅ Updated machine count to {machines_count} from assessment for user {user_id}")
                
        except Exception as e:
            logger.error(f"❌ Error updating progress from assessment: {e}")
    
    def save_roadmap(self, user_id: str, roadmap: str, certification: Optional[str] = None):
        """
        Save generated roadmap for a user.
        
        Args:
            user_id: Discord user ID
            roadmap: Generated roadmap text
            certification: Certification code to store roadmap under (optional)
        """
        user_id = str(user_id)
        
        if user_id not in self.users:
            self.create_user(user_id)
        
        roadmap_data = {
            'content': roadmap,
            'generated_at': datetime.now().isoformat()
        }
        
        # Legacy single-roadmap field (kept for backward compatibility)
        self.users[user_id]['roadmap'] = roadmap_data
        
        # Per-certification roadmap storage
        if certification:
            if 'roadmaps' not in self.users[user_id]:
                self.users[user_id]['roadmaps'] = {}
            self.users[user_id]['roadmaps'][certification.upper()] = roadmap_data
        
        # Add to history
        if 'history' not in self.users[user_id]:
            self.users[user_id]['history'] = {'assessments': [], 'roadmaps_generated': []}
        
        cert_for_history = certification or (self.users[user_id].get('assessment_results') or {}).get('certification')
        self.users[user_id]['history']['roadmaps_generated'].append({
            'certification': cert_for_history,
            'timestamp': roadmap_data['generated_at']
        })
        
        # Update last active
        self.users[user_id]['last_active'] = datetime.now().isoformat()
        
        self._save_data()
        
        logger.info(f"✅ Saved roadmap for user {user_id}" + (f" [{certification}]" if certification else ""))
    
    def save_roadmap_for_cert(self, user_id: str, certification: str, roadmap: str):
        """
        Save a roadmap specifically for a certification.
        
        Args:
            user_id: Discord user ID
            certification: Certification code (e.g., 'OSCP')
            roadmap: Generated roadmap text
        """
        self.save_roadmap(user_id, roadmap, certification=certification.upper())
    
    def get_roadmap_for_cert(self, user_id: str, certification: str) -> Optional[str]:
        """
        Get the saved roadmap for a specific certification.
        
        Args:
            user_id: Discord user ID
            certification: Certification code (e.g., 'OSCP')
            
        Returns:
            Roadmap content string or None if not found
        """
        user_id = str(user_id)
        user_data = self.get_user_data(user_id)
        
        if not user_data:
            return None
        
        cert_upper = certification.upper()
        
        # Check per-cert roadmaps dict first
        roadmaps = user_data.get('roadmaps', {})
        if cert_upper in roadmaps:
            roadmap_data = roadmaps[cert_upper]
            return roadmap_data.get('content') if isinstance(roadmap_data, dict) else roadmap_data
        
        return None
    
    def update_progress(
        self,
        user_id: str,
        machines_completed: Optional[int] = None,
        hours_studied: Optional[float] = None,
        current_phase: Optional[int] = None,
        milestone: Optional[str] = None
    ):
        """
        Update user's progress.
        
        Args:
            user_id: Discord user ID
            machines_completed: Number of machines completed (optional)
            hours_studied: Hours studied (optional)
            current_phase: Current study phase (optional)
            milestone: Milestone to add (optional)
        """
        user_id = str(user_id)
        
        if user_id not in self.users:
            self.create_user(user_id)
        
        progress = self.users[user_id].get('progress', {})
        
        if machines_completed is not None:
            progress['machines_completed'] = machines_completed
        
        if hours_studied is not None:
            progress['hours_studied'] = hours_studied
        
        if current_phase is not None:
            progress['current_phase'] = current_phase
        
        if milestone:
            if 'milestones_completed' not in progress:
                progress['milestones_completed'] = []
            
            milestone_data = {
                'title': milestone,
                'completed_at': datetime.now().isoformat()
            }
            progress['milestones_completed'].append(milestone_data)
        
        self.users[user_id]['progress'] = progress
        self.users[user_id]['last_active'] = datetime.now().isoformat()
        
        self._save_data()
        
        logger.info(f"✅ Updated progress for user {user_id}")
    
    def get_progress(self, user_id: str) -> Dict[str, Any]:
        """
        Get user's progress.
        
        Args:
            user_id: Discord user ID
            
        Returns:
            Progress dictionary
        """
        user_id = str(user_id)
        user_data = self.get_user_data(user_id)
        
        if not user_data:
            return {
                'machines_completed': 0,
                'hours_studied': 0,
                'current_phase': 1,
                'milestones_completed': []
            }
        
        return user_data.get('progress', {
            'machines_completed': 0,
            'hours_studied': 0,
            'current_phase': 1,
            'milestones_completed': []
        })
    
    def set_preference(
        self,
        user_id: str,
        preference_key: str,
        value: Any
    ):
        """
        Set a user preference.
        
        Args:
            user_id: Discord user ID
            preference_key: Preference key
            value: Preference value
        """
        user_id = str(user_id)
        
        if user_id not in self.users:
            self.create_user(user_id)
        
        if 'preferences' not in self.users[user_id]:
            self.users[user_id]['preferences'] = {}
        
        self.users[user_id]['preferences'][preference_key] = value
        self.users[user_id]['last_active'] = datetime.now().isoformat()
        
        self._save_data()
        
        logger.info(f"✅ Set preference for user {user_id}: {preference_key} = {value}")
    
    def get_preference(
        self,
        user_id: str,
        preference_key: str,
        default: Any = None
    ) -> Any:
        """
        Get a user preference.
        
        Args:
            user_id: Discord user ID
            preference_key: Preference key
            default: Default value if not set
            
        Returns:
            Preference value or default
        """
        user_id = str(user_id)
        user_data = self.get_user_data(user_id)
        
        if not user_data:
            return default
        
        preferences = user_data.get('preferences', {})
        return preferences.get(preference_key, default)
    
    def get_assessment_history(self, user_id: str) -> List[Dict[str, Any]]:
        """
        Get user's assessment history.
        
        Args:
            user_id: Discord user ID
            
        Returns:
            List of assessment history entries
        """
        user_id = str(user_id)
        user_data = self.get_user_data(user_id)
        
        if not user_data:
            return []
        
        history = user_data.get('history', {})
        return history.get('assessments', [])
    
    def get_roadmap_history(self, user_id: str) -> List[Dict[str, Any]]:
        """
        Get user's roadmap generation history.
        
        Args:
            user_id: Discord user ID
            
        Returns:
            List of roadmap history entries
        """
        user_id = str(user_id)
        user_data = self.get_user_data(user_id)
        
        if not user_data:
            return []
        
        history = user_data.get('history', {})
        return history.get('roadmaps_generated', [])
    
    def delete_user(self, user_id: str) -> bool:
        """
        Delete a user's data.
        
        Args:
            user_id: Discord user ID
            
        Returns:
            True if deleted, False if user not found
        """
        user_id = str(user_id)
        
        if user_id in self.users:
            del self.users[user_id]
            self._save_data()
            logger.info(f"🗑️ Deleted user data: {user_id}")
            return True
        
        return False
    
    def get_all_users(self) -> List[str]:
        """
        Get list of all user IDs.
        
        Returns:
            List of user IDs
        """
        return list(self.users.keys())
    
    def get_user_count(self) -> int:
        """
        Get total number of users.
        
        Returns:
            User count
        """
        return len(self.users)
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Get overall statistics across all users.
        
        Returns:
            Statistics dictionary
        """
        total_users = len(self.users)
        
        if total_users == 0:
            return {
                'total_users': 0,
                'total_assessments': 0,
                'total_roadmaps': 0,
                'total_machines_completed': 0,
                'total_hours_studied': 0,
                'certifications': {},
                'average_score': 0,
                'skill_levels': {}
            }
        
        total_assessments = 0
        total_roadmaps = 0
        total_machines = 0
        total_hours = 0
        certifications = {}
        scores = []
        skill_levels = {}
        
        for user_data in self.users.values():
            # Count assessments
            history = user_data.get('history', {})
            assessments = history.get('assessments', [])
            total_assessments += len(assessments)
            
            # Count roadmaps
            roadmaps = history.get('roadmaps_generated', [])
            total_roadmaps += len(roadmaps)
            
            # Current assessment data
            assessment = user_data.get('assessment_results', {})
            if assessment:
                cert = assessment.get('certification')
                if cert:
                    certifications[cert] = certifications.get(cert, 0) + 1
                
                score = assessment.get('score_percentage')
                if score:
                    scores.append(score)
                
                skill_level = assessment.get('skill_level')
                if skill_level:
                    skill_levels[skill_level] = skill_levels.get(skill_level, 0) + 1
            
            # Progress data
            progress = user_data.get('progress', {})
            total_machines += progress.get('machines_completed', 0)
            total_hours += progress.get('hours_studied', 0)
        
        avg_score = sum(scores) / len(scores) if scores else 0
        
        return {
            'total_users': total_users,
            'total_assessments': total_assessments,
            'total_roadmaps': total_roadmaps,
            'total_machines_completed': total_machines,
            'total_hours_studied': round(total_hours, 1),
            'certifications': certifications,
            'average_score': round(avg_score, 1),
            'skill_levels': skill_levels
        }
    
    def get_leaderboard(self, metric: str = 'machines', limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get leaderboard based on a metric.
        
        Args:
            metric: Metric to rank by ('machines', 'hours', 'score')
            limit: Number of users to return
            
        Returns:
            List of user rankings
        """
        leaderboard = []
        
        for user_id, user_data in self.users.items():
            entry = {
                'user_id': user_id,
                'username': user_data.get('username', 'Unknown')
            }
            
            if metric == 'machines':
                progress = user_data.get('progress', {})
                entry['value'] = progress.get('machines_completed', 0)
                entry['label'] = 'machines'
            
            elif metric == 'hours':
                progress = user_data.get('progress', {})
                entry['value'] = progress.get('hours_studied', 0)
                entry['label'] = 'hours'
            
            elif metric == 'score':
                assessment = user_data.get('assessment_results', {})
                entry['value'] = assessment.get('score_percentage', 0)
                entry['label'] = 'score'
            
            leaderboard.append(entry)
        
        # Sort by value descending
        leaderboard.sort(key=lambda x: x['value'], reverse=True)
        
        # Return top N
        return leaderboard[:limit]
    
    def export_user_data(self, user_id: str) -> Optional[str]:
        """
        Export user data as JSON string.
        
        Args:
            user_id: Discord user ID
            
        Returns:
            JSON string of user data or None
        """
        user_id = str(user_id)
        user_data = self.get_user_data(user_id)
        
        if not user_data:
            return None
        
        try:
            return json.dumps(user_data, indent=2, ensure_ascii=False)
        except Exception as e:
            logger.error(f"❌ Error exporting user data: {e}")
            return None
    
    def import_user_data(self, user_id: str, json_data: str) -> bool:
        """
        Import user data from JSON string.
        
        Args:
            user_id: Discord user ID
            json_data: JSON string of user data
            
        Returns:
            True if successful, False otherwise
        """
        user_id = str(user_id)
        
        try:
            user_data = json.loads(json_data)
            user_data['user_id'] = user_id  # Ensure correct user_id
            self.users[user_id] = user_data
            self._save_data()
            logger.info(f"✅ Imported data for user {user_id}")
            return True
        except Exception as e:
            logger.error(f"❌ Error importing user data: {e}")
            return False
    
    def backup_data(self, backup_path: Optional[Path] = None) -> bool:
        """
        Create a backup of all user data.
        
        Args:
            backup_path: Path for backup file (optional)
            
        Returns:
            True if successful, False otherwise
        """
        try:
            if not backup_path:
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                backup_path = self.storage_path.parent / f'user_data_backup_{timestamp}.json'
            
            with open(backup_path, 'w', encoding='utf-8') as f:
                json.dump(self.users, f, indent=2, ensure_ascii=False)
            
            logger.info(f"✅ Backup created: {backup_path}")
            return True
        except Exception as e:
            logger.error(f"❌ Error creating backup: {e}")
            return False
    
    def restore_from_backup(self, backup_path: Path) -> bool:
        """
        Restore user data from backup.
        
        Args:
            backup_path: Path to backup file
            
        Returns:
            True if successful, False otherwise
        """
        try:
            with open(backup_path, 'r', encoding='utf-8') as f:
                self.users = json.load(f)
            
            self._save_data()
            logger.info(f"✅ Restored from backup: {backup_path}")
            return True
        except Exception as e:
            logger.error(f"❌ Error restoring from backup: {e}")
            return False
    
    def clear_inactive_users(self, days: int = 90) -> int:
        """
        Clear users who haven't been active for specified days.
        
        Args:
            days: Number of days of inactivity
            
        Returns:
            Number of users removed
        """
        try:
            cutoff_date = datetime.now().timestamp() - (days * 24 * 60 * 60)
            removed = 0
            
            users_to_remove = []
            for user_id, user_data in self.users.items():
                last_active = user_data.get('last_active')
                if last_active:
                    try:
                        last_active_dt = datetime.fromisoformat(last_active)
                        if last_active_dt.timestamp() < cutoff_date:
                            users_to_remove.append(user_id)
                    except (ValueError, AttributeError):
                        pass  # Skip if date parsing fails
            
            for user_id in users_to_remove:
                del self.users[user_id]
                removed += 1
            
            if removed > 0:
                self._save_data()
                logger.info(f"🗑️ Removed {removed} inactive users (>{days} days)")
            
            return removed
        except Exception as e:
            logger.error(f"❌ Error clearing inactive users: {e}")
            return 0


# Utility function for testing
def test_user_manager():
    """Test user manager functionality."""
    print("🧪 Testing User Manager...")
    
    # Create test manager
    test_path = Path('test_user_data.json')
    manager = UserManager(str(test_path))
    
    # Create user
    user_id = 'test_user_123'
    user = manager.create_user(user_id, 'TestUser')
    print(f"✅ Created user: {user['username']}")
    
    # Save assessment
    assessment = {
        'certification': 'OSCP',
        'score_percentage': 75,
        'skill_level': 'Intermediate',
        'strengths': ['Linux', 'Networking'],
        'weaknesses': ['Web Exploitation']
    }
    manager.save_assessment_results(user_id, assessment)
    print(f"✅ Saved assessment: {assessment['score_percentage']}%")
    
    # Update progress
    manager.update_progress(user_id, machines_completed=15, hours_studied=45.5)
    print(f"✅ Updated progress: 15 machines, 45.5 hours")
    
    # Get statistics
    stats = manager.get_statistics()
    print(f"\n📊 Statistics:")
    print(f"Total Users: {stats['total_users']}")
    print(f"Total Assessments: {stats['total_assessments']}")
    print(f"Average Score: {stats['average_score']}%")
    
    # Cleanup
    test_path.unlink(missing_ok=True)
    print("\n✅ Test completed!")


if __name__ == "__main__":
    test_user_manager()