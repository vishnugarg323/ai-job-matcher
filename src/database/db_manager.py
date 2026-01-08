"""
Database manager for storing and retrieving job data.
"""

import sqlite3
from pathlib import Path
from datetime import datetime, timedelta
import json
import hashlib
from utils.logger import setup_logger

logger = setup_logger(__name__)


class DatabaseManager:
    """Manage job database operations."""
    
    def __init__(self, config):
        """
        Initialize database manager.
        
        Args:
            config: Application configuration
        """
        self.config = config
        self.db_path = Path(config['database']['path'])
        self.db_path.parent.mkdir(exist_ok=True)
        self._initialize_database()
    
    def _initialize_database(self):
        """Create database tables if they don't exist."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Jobs table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS jobs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                job_hash TEXT UNIQUE NOT NULL,
                title TEXT NOT NULL,
                company TEXT NOT NULL,
                location TEXT,
                url TEXT NOT NULL,
                description TEXT,
                salary TEXT,
                posted_date TEXT,
                source TEXT NOT NULL,
                match_score REAL,
                keywords_matched TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                notified BOOLEAN DEFAULT 0,
                notification_sent_at TIMESTAMP
            )
        ''')
        
        # Index for faster queries
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_job_hash ON jobs(job_hash)
        ''')
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_created_at ON jobs(created_at)
        ''')
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_match_score ON jobs(match_score)
        ''')
        
        conn.commit()
        conn.close()
        
        logger.info(f"✓ Database initialized at {self.db_path}")
    
    def _generate_job_hash(self, job):
        """
        Generate unique hash for a job.
        
        Args:
            job: Job dictionary
            
        Returns:
            Hash string
        """
        # Use title + company + location for uniqueness
        unique_string = f"{job['title']}|{job['company']}|{job.get('location', '')}"
        return hashlib.md5(unique_string.encode()).hexdigest()
    
    def filter_new_jobs(self, jobs):
        """
        Filter out jobs that already exist in database.
        
        Args:
            jobs: List of job dictionaries
            
        Returns:
            List of new jobs
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        new_jobs = []
        for job in jobs:
            job_hash = self._generate_job_hash(job)
            
            cursor.execute('SELECT id FROM jobs WHERE job_hash = ?', (job_hash,))
            if not cursor.fetchone():
                job['job_hash'] = job_hash
                new_jobs.append(job)
        
        conn.close()
        return new_jobs
    
    def get_unnotified_jobs(self, min_score=0.9):
        """
        Get jobs that haven't been sent in email yet.
        
        Args:
            min_score: Minimum match score
            
        Returns:
            List of new job dictionaries
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM jobs 
            WHERE notified = 0 AND match_score >= ?
            ORDER BY match_score DESC
            LIMIT 10
        ''', (min_score,))
        
        jobs = [dict(row) for row in cursor.fetchall()]
        conn.close()
        
        return jobs
    
    def mark_jobs_notified(self, job_ids):
        """
        Mark jobs as notified after sending email.
        
        Args:
            job_ids: List of job IDs that were sent
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        for job_id in job_ids:
            cursor.execute('''
                UPDATE jobs 
                SET notified = 1, notification_sent_at = CURRENT_TIMESTAMP
                WHERE id = ?
            ''', (job_id,))
        
        conn.commit()
        conn.close()
        
        logger.info(f"✓ Marked {len(job_ids)} jobs as notified")
    
    def save_jobs(self, jobs):
        """
        Save matched jobs to database.
        
        Args:
            jobs: List of job dictionaries with match scores
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        saved_count = 0
        for job in jobs:
            try:
                cursor.execute('''
                    INSERT OR IGNORE INTO jobs 
                    (job_hash, title, company, location, url, description, 
                     salary, posted_date, source, match_score, keywords_matched)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    job['job_hash'],
                    job['title'],
                    job['company'],
                    job.get('location'),
                    job['url'],
                    job.get('description'),
                    job.get('salary'),
                    job.get('posted_date'),
                    job['source'],
                    job.get('match_score'),
                    json.dumps(job.get('keywords_matched', []))
                ))
                saved_count += 1
            except Exception as e:
                logger.error(f"Error saving job {job.get('title')}: {e}")
        
        conn.commit()
        conn.close()
        
        logger.info(f"💾 Saved {saved_count} jobs to database")
    
    def get_recent_jobs(self, days=7, min_score=0.9):
        """
        Get recent jobs with high match scores.
        
        Args:
            days: Number of days to look back
            min_score: Minimum match score
            
        Returns:
            List of job dictionaries
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cutoff_date = (datetime.now() - timedelta(days=days)).isoformat()
        
        cursor.execute('''
            SELECT * FROM jobs 
            WHERE created_at >= ? AND match_score >= ?
            ORDER BY match_score DESC, created_at DESC
        ''', (cutoff_date, min_score))
        
        jobs = [dict(row) for row in cursor.fetchall()]
        conn.close()
        
        return jobs
    
    def cleanup_old_jobs(self):
        """Remove jobs older than retention period."""
        retention_days = self.config['database']['retention_days']
        cutoff_date = (datetime.now() - timedelta(days=retention_days)).isoformat()
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM jobs WHERE created_at < ?', (cutoff_date,))
        deleted = cursor.rowcount
        
        conn.commit()
        conn.close()
        
        if deleted > 0:
            logger.info(f"🧹 Cleaned up {deleted} old jobs")
