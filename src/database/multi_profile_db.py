"""
Enhanced Database Manager with Multi-Profile Support
"""

import sqlite3
from pathlib import Path
from datetime import datetime, timedelta
import json
import hashlib
from typing import List, Dict, Optional

class DatabaseManager:
    """Manage multi-profile job database operations."""
    
    def __init__(self, db_path='data/jobs.db'):
        """Initialize database manager"""
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._initialize_database()
    
    def _initialize_database(self):
        """Create database tables if they don't exist"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Profiles table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS profiles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                resume_path TEXT,
                gemini_key TEXT,
                job_preferences TEXT,
                enabled BOOLEAN DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Jobs table (with profile_id)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS jobs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                profile_id INTEGER NOT NULL,
                job_hash TEXT NOT NULL,
                title TEXT NOT NULL,
                company TEXT NOT NULL,
                location TEXT,
                url TEXT NOT NULL,
                description TEXT,
                salary TEXT,
                posted_date TEXT,
                source TEXT NOT NULL,
                match_score REAL,
                ai_similarity REAL,
                keyword_match REAL,
                urgency_score REAL,
                keywords_matched TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                notified BOOLEAN DEFAULT 0,
                notification_sent_at TIMESTAMP,
                FOREIGN KEY (profile_id) REFERENCES profiles(id) ON DELETE CASCADE,
                UNIQUE(profile_id, job_hash)
            )
        ''')
        
        # Run history table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS run_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                profile_id INTEGER NOT NULL,
                status TEXT NOT NULL,
                jobs_found INTEGER DEFAULT 0,
                jobs_scraped INTEGER DEFAULT 0,
                error_message TEXT,
                started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                completed_at TIMESTAMP,
                FOREIGN KEY (profile_id) REFERENCES profiles(id) ON DELETE CASCADE
            )
        ''')
        
        # Indexes
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_profile_jobs ON jobs(profile_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_job_hash ON jobs(job_hash)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_created_at ON jobs(created_at)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_match_score ON jobs(match_score)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_run_history ON run_history(profile_id)')
        
        conn.commit()
        conn.close()
    
    # ==================== PROFILE MANAGEMENT ====================
    
    def create_profile(self, name: str, email: str, gemini_key: str = None, 
                      job_preferences: dict = None) -> int:
        """Create a new profile"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO profiles (name, email, gemini_key, job_preferences)
            VALUES (?, ?, ?, ?)
        ''', (name, email, gemini_key, json.dumps(job_preferences or {})))
        
        profile_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return profile_id
    
    def get_profile(self, profile_id: int) -> Optional[Dict]:
        """Get profile by ID"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM profiles WHERE id = ?', (profile_id,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            profile = dict(row)
            profile['job_preferences'] = json.loads(profile['job_preferences'] or '{}')
            return profile
        return None
    
    def get_all_profiles(self) -> List[Dict]:
        """Get all profiles"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM profiles ORDER BY created_at DESC')
        rows = cursor.fetchall()
        conn.close()
        
        profiles = []
        for row in rows:
            profile = dict(row)
            profile['job_preferences'] = json.loads(profile['job_preferences'] or '{}')
            profiles.append(profile)
        
        return profiles
    
    def update_profile(self, profile_id: int, name: str = None, email: str = None,
                      gemini_key: str = None, job_preferences: dict = None):
        """Update profile fields"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        updates = []
        params = []
        
        if name is not None:
            updates.append('name = ?')
            params.append(name)
        if email is not None:
            updates.append('email = ?')
            params.append(email)
        if gemini_key is not None:
            updates.append('gemini_key = ?')
            params.append(gemini_key)
        if job_preferences is not None:
            updates.append('job_preferences = ?')
            params.append(json.dumps(job_preferences))
        
        if updates:
            updates.append('updated_at = CURRENT_TIMESTAMP')
            params.append(profile_id)
            
            cursor.execute(f'''
                UPDATE profiles SET {', '.join(updates)}
                WHERE id = ?
            ''', params)
        
        conn.commit()
        conn.close()
    
    def update_profile_resume(self, profile_id: int, resume_path: str):
        """Update profile resume path"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE profiles SET resume_path = ?, updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        ''', (resume_path, profile_id))
        
        conn.commit()
        conn.close()
    
    def delete_profile(self, profile_id: int):
        """Delete a profile (cascade deletes jobs and history)"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM profiles WHERE id = ?', (profile_id,))
        
        conn.commit()
        conn.close()
    
    def toggle_profile(self, profile_id: int, enabled: bool):
        """Enable/disable a profile"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE profiles SET enabled = ?, updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        ''', (enabled, profile_id))
        
        conn.commit()
        conn.close()
    
    # ==================== JOB MANAGEMENT ====================
    
    def save_jobs(self, profile_id: int, jobs: List[Dict]) -> int:
        """Save jobs for a profile"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        saved_count = 0
        for job in jobs:
            job_hash = self._generate_job_hash(job)
            
            try:
                cursor.execute('''
                    INSERT INTO jobs (
                        profile_id, job_hash, title, company, location, url,
                        description, salary, posted_date, source, match_score,
                        ai_similarity, keyword_match, urgency_score, keywords_matched
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    profile_id, job_hash, job['title'], job['company'],
                    job.get('location'), job['url'], job.get('description'),
                    job.get('salary'), job.get('posted_date'), job['source'],
                    job.get('match_score'), job.get('ai_similarity'),
                    job.get('keyword_match'), job.get('urgency_score'),
                    json.dumps(job.get('keywords_matched', []))
                ))
                saved_count += 1
            except sqlite3.IntegrityError:
                # Job already exists for this profile
                pass
        
        conn.commit()
        conn.close()
        
        return saved_count
    
    def get_profile_jobs(self, profile_id: int, limit: int = 50) -> List[Dict]:
        """Get jobs for a profile"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM jobs
            WHERE profile_id = ?
            ORDER BY match_score DESC, created_at DESC
            LIMIT ?
        ''', (profile_id, limit))
        
        rows = cursor.fetchall()
        conn.close()
        
        jobs = []
        for row in rows:
            job = dict(row)
            job['keywords_matched'] = json.loads(job['keywords_matched'] or '[]')
            jobs.append(job)
        
        return jobs
    
    def get_unnotified_jobs(self, profile_id: int, limit: int = 10) -> List[Dict]:
        """Get unnotified jobs for a profile"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM jobs
            WHERE profile_id = ? AND notified = 0
            ORDER BY match_score DESC, urgency_score DESC, created_at DESC
            LIMIT ?
        ''', (profile_id, limit))
        
        rows = cursor.fetchall()
        conn.close()
        
        jobs = []
        for row in rows:
            job = dict(row)
            job['keywords_matched'] = json.loads(job['keywords_matched'] or '[]')
            jobs.append(job)
        
        return jobs
    
    def mark_jobs_notified(self, job_ids: List[int]):
        """Mark jobs as notified"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        placeholders = ','.join('?' * len(job_ids))
        cursor.execute(f'''
            UPDATE jobs
            SET notified = 1, notification_sent_at = CURRENT_TIMESTAMP
            WHERE id IN ({placeholders})
        ''', job_ids)
        
        conn.commit()
        conn.close()
    
    def _generate_job_hash(self, job: Dict) -> str:
        """Generate unique hash for a job"""
        unique_string = f"{job['title']}|{job['company']}|{job.get('location', '')}"
        return hashlib.md5(unique_string.encode()).hexdigest()
    
    # ==================== RUN HISTORY ====================
    
    def create_run_record(self, profile_id: int, status: str = 'running') -> int:
        """Create a run history record"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO run_history (profile_id, status)
            VALUES (?, ?)
        ''', (profile_id, status))
        
        run_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return run_id
    
    def update_run_record(self, run_id: int, status: str = None,
                         jobs_found: int = None, jobs_scraped: int = None,
                         error_message: str = None):
        """Update a run history record"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        updates = ['completed_at = CURRENT_TIMESTAMP']
        params = []
        
        if status is not None:
            updates.append('status = ?')
            params.append(status)
        if jobs_found is not None:
            updates.append('jobs_found = ?')
            params.append(jobs_found)
        if jobs_scraped is not None:
            updates.append('jobs_scraped = ?')
            params.append(jobs_scraped)
        if error_message is not None:
            updates.append('error_message = ?')
            params.append(error_message)
        
        params.append(run_id)
        
        cursor.execute(f'''
            UPDATE run_history SET {', '.join(updates)}
            WHERE id = ?
        ''', params)
        
        conn.commit()
        conn.close()
    
    def get_run_history(self, profile_id: int, limit: int = 10) -> List[Dict]:
        """Get run history for a profile"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM run_history
            WHERE profile_id = ?
            ORDER BY started_at DESC
            LIMIT ?
        ''', (profile_id, limit))
        
        rows = cursor.fetchall()
        conn.close()
        
        return [dict(row) for row in rows]
    
    # ==================== DASHBOARD STATS ====================
    
    def get_dashboard_stats(self) -> Dict:
        """Get overall dashboard statistics"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Total profiles
        cursor.execute('SELECT COUNT(*) FROM profiles WHERE enabled = 1')
        total_profiles = cursor.fetchone()[0]
        
        # Total jobs (last 7 days)
        cursor.execute('''
            SELECT COUNT(*) FROM jobs
            WHERE created_at >= datetime('now', '-7 days')
        ''')
        jobs_last_7_days = cursor.fetchone()[0]
        
        # Success rate (last 10 runs)
        cursor.execute('''
            SELECT 
                COUNT(CASE WHEN status = 'success' THEN 1 END) * 100.0 / COUNT(*) as success_rate
            FROM (
                SELECT status FROM run_history
                ORDER BY started_at DESC
                LIMIT 10
            )
        ''')
        result = cursor.fetchone()
        success_rate = result[0] if result[0] is not None else 0
        
        # Average jobs per run
        cursor.execute('''
            SELECT AVG(jobs_found) FROM run_history
            WHERE status = 'success' AND started_at >= datetime('now', '-7 days')
        ''')
        result = cursor.fetchone()
        avg_jobs_per_run = result[0] if result[0] is not None else 0
        
        conn.close()
        
        return {
            'total_profiles': total_profiles,
            'jobs_last_7_days': jobs_last_7_days,
            'success_rate': round(success_rate, 1),
            'avg_jobs_per_run': round(avg_jobs_per_run, 1)
        }
