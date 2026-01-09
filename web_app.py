"""
Multi-Profile Job Matcher Web Application
Flask-based web UI for managing multiple resume profiles
"""

import os
import sys
import yaml
from datetime import datetime
from pathlib import Path
from flask import Flask, render_template, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
import threading
import time
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
import pytz

# Add src directory to path for imports
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from database.multi_profile_db import DatabaseManager
from matchers.resume_parser import ResumeParser
from matchers.job_matcher import JobMatcher
from scrapers.indeed_scraper import IndeedScraper
from scrapers.stepstone_scraper import StepStoneScraper
from scrapers.linkedin_scraper import LinkedInScraper
from notifiers.email_notifier import EmailNotifier
from utils.logger import setup_logger

logger = setup_logger(__name__)

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['UPLOAD_FOLDER'] = 'data/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Ensure upload folder exists
Path(app.config['UPLOAD_FOLDER']).mkdir(parents=True, exist_ok=True)

# Initialize database
db_manager = DatabaseManager()

# Store running jobs
active_jobs = {}

# Initialize scheduler
scheduler = BackgroundScheduler()
scheduler.start()


@app.route('/')
def index():
    """Main dashboard page"""
    return render_template('dashboard.html')


@app.route('/api/profiles', methods=['GET'])
def get_profiles():
    """Get all job search profiles"""
    try:
        profiles = db_manager.get_all_profiles()
        return jsonify({
            'success': True,
            'profiles': profiles
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/profiles', methods=['POST'])
def create_profile():
    """Create a new job search profile"""
    try:
        data = request.json
        profile_id = db_manager.create_profile(
            name=data['name'],
            email=data['email'],
            gemini_key=data.get('gemini_key', os.getenv('GEMINI_API_KEY')),
            job_preferences=data.get('job_preferences', {})
        )
        return jsonify({
            'success': True,
            'profile_id': profile_id,
            'message': 'Profile created successfully'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/profiles/<int:profile_id>', methods=['PUT'])
def update_profile(profile_id):
    """Update an existing profile"""
    try:
        data = request.json
        db_manager.update_profile(
            profile_id=profile_id,
            name=data.get('name'),
            email=data.get('email'),
            gemini_key=data.get('gemini_key'),
            job_preferences=data.get('job_preferences')
        )
        return jsonify({
            'success': True,
            'message': 'Profile updated successfully'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/profiles/<int:profile_id>', methods=['DELETE'])
def delete_profile(profile_id):
    """Delete a profile"""
    try:
        db_manager.delete_profile(profile_id)
        return jsonify({
            'success': True,
            'message': 'Profile deleted successfully'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/profiles/<int:profile_id>/resume', methods=['POST'])
def upload_resume(profile_id):
    """Upload resume for a profile"""
    try:
        if 'resume' not in request.files:
            return jsonify({
                'success': False,
                'error': 'No file provided'
            }), 400
        
        file = request.files['resume']
        if file.filename == '':
            return jsonify({
                'success': False,
                'error': 'No file selected'
            }), 400
        
        if file and allowed_file(file.filename):
            filename = secure_filename(f"profile_{profile_id}_{file.filename}")
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            # Update profile with resume path
            db_manager.update_profile_resume(profile_id, filepath)
            
            return jsonify({
                'success': True,
                'message': 'Resume uploaded successfully',
                'filename': filename
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Invalid file type. Only PDF, DOCX allowed'
            }), 400
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/profiles/<int:profile_id>/run', methods=['POST'])
def trigger_job_search(profile_id):
    """Manually trigger job search for a profile"""
    try:
        # Check if profile exists
        profile = db_manager.get_profile(profile_id)
        if not profile:
            return jsonify({
                'success': False,
                'error': 'Profile not found'
            }), 404
        
        # Check if already running
        if profile_id in active_jobs:
            return jsonify({
                'success': False,
                'error': 'Job search already running for this profile'
            }), 409
        
        # Start job search in background
        thread = threading.Thread(
            target=run_job_search_for_profile,
            args=(profile_id, profile)
        )
        thread.start()
        active_jobs[profile_id] = thread
        
        return jsonify({
            'success': True,
            'message': 'Job search started',
            'profile_id': profile_id
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/profiles/<int:profile_id>/jobs', methods=['GET'])
def get_profile_jobs(profile_id):
    """Get jobs found for a profile"""
    try:
        limit = request.args.get('limit', 50, type=int)
        jobs = db_manager.get_profile_jobs(profile_id, limit=limit)
        return jsonify({
            'success': True,
            'jobs': jobs,
            'count': len(jobs)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/profiles/<int:profile_id>/history', methods=['GET'])
def get_profile_history(profile_id):
    """Get run history for a profile"""
    try:
        limit = request.args.get('limit', 10, type=int)
        history = db_manager.get_run_history(profile_id, limit=limit)
        return jsonify({
            'success': True,
            'history': history
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/dashboard/stats', methods=['GET'])
def get_dashboard_stats():
    """Get overall dashboard statistics"""
    try:
        stats = db_manager.get_dashboard_stats()
        return jsonify({
            'success': True,
            'stats': stats
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/config', methods=['GET'])
def get_config():
    """Get global configuration"""
    try:
        # Return non-sensitive config
        config = {
            'schedule_interval': os.getenv('SCHEDULE_INTERVAL_MINUTES', 30),
            'max_jobs_per_email': os.getenv('MAX_JOBS_PER_EMAIL', 10),
            'job_age_days': os.getenv('MAX_JOB_AGE_DAYS', 14)
        }
        return jsonify({
            'success': True,
            'config': config
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint for Railway"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat()
    })


def allowed_file(filename):
    """Check if file extension is allowed"""
    ALLOWED_EXTENSIONS = {'pdf', 'docx', 'doc'}
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def run_job_search_for_profile(profile_id, profile):
    """Run job search for a specific profile (background task)"""
    try:
        logger.info(f"🚀 Starting job search for profile: {profile['name']}")
        
        # Record run start
        run_id = db_manager.create_run_record(profile_id, 'running')
        
        # Load configuration
        config = load_config()
        
        # Override with profile-specific settings
        if profile.get('job_preferences'):
            prefs = profile['job_preferences'] if isinstance(profile['job_preferences'], dict) else {}
            if prefs:
                config['search'].update(prefs)
        
        # Initialize resume parser
        resume_parser = ResumeParser(config)
        resume_parser.resume_path = Path(profile['resume_path'])
        resume_text = resume_parser.parse_resume()
        
        if not resume_text:
            raise ValueError("Failed to parse resume")
        
        # Set Gemini API key (profile-specific or global)
        gemini_key = profile.get('gemini_key') or os.getenv('GEMINI_API_KEY')
        if gemini_key:
            os.environ['GEMINI_API_KEY'] = gemini_key
        
        # Initialize job matcher
        job_matcher = JobMatcher(config, resume_parser)
        
        # Scrape jobs from all sources
        scrapers = [
            IndeedScraper(config),
            StepStoneScraper(config),
        ]
        
        # Add LinkedIn if credentials available
        if os.getenv('LINKEDIN_EMAIL') and os.getenv('LINKEDIN_PASSWORD'):
            scrapers.append(LinkedInScraper(config))
            logger.info("✓ LinkedIn scraper enabled")
        else:
            logger.info("ℹ️ LinkedIn disabled - set LINKEDIN_EMAIL/PASSWORD to enable")
        
        all_jobs = []
        jobs_scraped = 0
        
        for scraper in scrapers:
            try:
                jobs = scraper.scrape_jobs()
                all_jobs.extend(jobs)
                jobs_scraped += len(jobs)
                logger.info(f"✓ Scraped {len(jobs)} jobs from {scraper.__class__.__name__}")
            except Exception as e:
                logger.error(f"✗ {scraper.__class__.__name__} failed: {e}")
        
        # Match jobs
        matched_jobs = job_matcher.match_jobs(all_jobs)
        logger.info(f"🎯 Matched {len(matched_jobs)} jobs")
        
        # Save to database
        saved = db_manager.save_jobs(profile_id, matched_jobs)
        logger.info(f"💾 Saved {saved} new jobs")
        
        # Send email notification if matches found and email configured
        if matched_jobs and os.getenv('EMAIL_SENDER') and os.getenv('EMAIL_PASSWORD'):
            unnotified = db_manager.get_unnotified_jobs(profile_id, limit=10)
            if unnotified:
                try:
                    notifier = EmailNotifier(config)
                    notifier.config['notifications']['email'] = profile['email']
                    notifier.send_job_matches(unnotified)
                    
                    # Mark as notified
                    job_ids = [job['id'] for job in unnotified]
                    db_manager.mark_jobs_notified(job_ids)
                    logger.info(f"📧 Sent email with {len(unnotified)} jobs to {profile['email']}")
                except Exception as e:
                    logger.warning(f"⚠️ Email sending failed (not critical): {e}")
        elif matched_jobs:
            logger.info(f"ℹ️ Found {len(matched_jobs)} jobs - email not configured, view in dashboard")
        
        # Update run record
        db_manager.update_run_record(
            run_id,
            status='success',
            jobs_found=len(matched_jobs),
            jobs_scraped=jobs_scraped
        )
        
        logger.info(f"✅ Job search completed for {profile['name']}")
        
    except Exception as e:
        logger.error(f"❌ Error in job search: {e}", exc_info=True)
        db_manager.update_run_record(
            run_id,
            status='failed',
            error_message=str(e)
        )
    finally:
        # Remove from active jobs
        if profile_id in active_jobs:
            del active_jobs[profile_id]


def load_config():
    """Load configuration from config.yaml"""
    config_path = Path('config/config.yaml')
    if config_path.exists():
        with open(config_path, 'r') as f:
            return yaml.safe_load(f)
    
    # Return default config if file doesn't exist
    return {
        'search': {
            'job_titles': ['Software Engineer', 'Python Developer'],
            'locations': ['Berlin', 'Munich', 'Remote'],
            'max_job_age_days': 14
        },
        'matching': {
            'threshold': 0.90,
            'gemini_embedding_model': 'models/text-embedding-004',
            'use_gemini_pro': True,
            'gemini_chat_model': 'gemini-1.5-pro',
            'weights': {
                'skills': 0.40,
                'experience': 0.30,
                'education': 0.15,
                'description_match': 0.15
            }
        },
        'scraping': {
            'enabled_scrapers': ['indeed', 'stepstone', 'linkedin'],
            'max_pages': 5,
            'request_delay': 2,
            'timeout': 30,
            'headless': True
        },
        'notifications': {
            'enabled': True,
            'max_jobs_per_email': 10
        },
        'database': {
            'path': 'data/jobs.db'
        }
    }


def run_scheduled_job_search():
    """Run job search for all enabled profiles (scheduled task)"""
    try:
        logger.info("⏰ Scheduled job search starting...")
        profiles = db_manager.get_all_profiles()
        
        enabled_profiles = [p for p in profiles if p.get('enabled', True) and p.get('resume_path')]
        
        if not enabled_profiles:
            logger.info("No enabled profiles with resumes. Skipping.")
            return
        
        logger.info(f"Found {len(enabled_profiles)} enabled profile(s)")
        
        for profile in enabled_profiles:
            if profile['id'] not in active_jobs:
                logger.info(f"Starting job search for: {profile['name']}")
                thread = threading.Thread(
                    target=run_job_search_for_profile,
                    args=(profile['id'], profile),
                    daemon=True
                )
                thread.start()
                active_jobs[profile['id']] = thread
                time.sleep(5)  # Stagger starts
            else:
                logger.info(f"Skipping {profile['name']} - already running")
        
    except Exception as e:
        logger.error(f"Error in scheduled job search: {e}", exc_info=True)


def load_profile_config(profile):
    """Load configuration for a profile"""
    base_config = load_config()
    
    # Merge profile preferences
    if profile.get('job_preferences'):
        prefs = profile['job_preferences'] if isinstance(profile['job_preferences'], dict) else {}
        base_config['search'].update(prefs)
    
    # Set profile email
    base_config['notifications']['email'] = profile['email']
    
    return base_config


if __name__ == '__main__':
    # Configure scheduler for automatic runs every 30 minutes
    scheduler.add_job(
        func=run_scheduled_job_search,
        trigger=IntervalTrigger(minutes=30),
        id='scheduled_job_search',
        name='Run job search for all profiles',
        replace_existing=True,
        timezone=pytz.UTC
    )
    
    logger.info("✅ Scheduler configured - will run every 30 minutes")
    logger.info(f"🌐 Starting web server on port {os.getenv('PORT', 5000)}")
    
    # Run initial job search on startup (optional - uncomment if desired)
    # threading.Thread(target=run_scheduled_job_search, daemon=True).start()
    
    # Railway provides PORT environment variable
    port = int(os.getenv('PORT', 5000))
    
    # Run Flask app
    app.run(
        host='0.0.0.0',
        port=port,
        debug=os.getenv('FLASK_ENV') == 'development'
    )
