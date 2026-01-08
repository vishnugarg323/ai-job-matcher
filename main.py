"""
Main entry point for the AI Job Matcher application.
"""

import os
import sys
import argparse
import logging
from pathlib import Path
from dotenv import load_dotenv

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from scheduler.job_scheduler import JobScheduler
from database.db_manager import DatabaseManager
from matchers.resume_parser import ResumeParser
from matchers.job_matcher import JobMatcher
from scrapers.indeed_scraper import IndeedScraper
from scrapers.stepstone_scraper import StepStoneScraper
from scrapers.linkedin_scraper import LinkedInScraper
from notifiers.email_notifier import EmailNotifier
from utils.config_loader import ConfigLoader
from utils.logger import setup_logger

# Load environment variables
load_dotenv()

# Setup logging
logger = setup_logger(__name__)


class JobMatcherApp:
    """Main application class for AI Job Matcher."""
    
    def __init__(self):
        """Initialize the application."""
        self.config = ConfigLoader.load_config()
        self.db_manager = DatabaseManager(self.config)
        self.resume_parser = ResumeParser(self.config)
        self.job_matcher = JobMatcher(self.config, self.resume_parser)
        self.email_notifier = EmailNotifier(self.config)
        self.scrapers = self._initialize_scrapers()
        
    def _initialize_scrapers(self):
        """Initialize enabled scrapers."""
        scrapers = []
        enabled = self.config['scraping']['enabled_scrapers']
        
        if 'indeed' in enabled:
            scrapers.append(IndeedScraper(self.config))
        if 'stepstone' in enabled:
            scrapers.append(StepStoneScraper(self.config))
        if 'linkedin' in enabled:
            scrapers.append(LinkedInScraper(self.config))
            
        return scrapers
    
    def run(self):
        """Run the job matching process once."""
        logger.info("🚀 Starting AI Job Matcher...")
        
        try:
            # Parse resume
            logger.info("📄 Parsing resume...")
            self.resume_parser.parse_resume()
            
            # Scrape jobs
            all_jobs = []
            for scraper in self.scrapers:
                logger.info(f"🔍 Scraping jobs from {scraper.name}...")
                jobs = scraper.scrape_jobs()
                logger.info(f"✓ Found {len(jobs)} jobs from {scraper.name}")
                all_jobs.extend(jobs)
            
            logger.info(f"📊 Total jobs scraped: {len(all_jobs)}")
            
            # Filter duplicates
            unique_jobs = self.db_manager.filter_new_jobs(all_jobs)
            logger.info(f"🆕 New jobs (not seen before): {len(unique_jobs)}")
            
            if not unique_jobs:
                logger.info("✓ No new jobs found. Exiting.")
                return
            
            # Match jobs
            logger.info("🎯 Matching jobs with resume...")
            matched_jobs = self.job_matcher.match_jobs(unique_jobs)
            logger.info(f"✨ Found {len(matched_jobs)} high-quality matches (≥90%)")
            
            if not matched_jobs:
                logger.info("✓ No matches found above threshold. Exiting.")
                return
            
            # Save to database
            logger.info("💾 Saving matches to database...")
            self.db_manager.save_jobs(matched_jobs)
            
            # Get only unnotified jobs to avoid sending duplicates
            unnotified_jobs = self.db_manager.get_unnotified_jobs()
            logger.info(f"📬 New jobs not yet sent: {len(unnotified_jobs)}")
            
            if not unnotified_jobs:
                logger.info("✓ All matches already sent in previous emails.")
                return
            
            # Send notification
            if self.config['notifications']['email_enabled']:
                logger.info("📧 Sending email notification...")
                self.email_notifier.send_notification(unnotified_jobs)
                
                # Mark as notified
                job_ids = [job['id'] for job in unnotified_jobs]
                self.db_manager.mark_jobs_notified(job_ids)
                
                logger.info("✓ Email sent successfully!")
            
            logger.info(f"✅ Job matching completed! {len(unnotified_jobs)} new matches sent.")
            
        except Exception as e:
            logger.error(f"❌ Error during job matching: {str(e)}", exc_info=True)
            raise
    
    def start_scheduler(self):
        """Start the scheduled job runner."""
        logger.info("⏰ Starting scheduled job runner...")
        scheduler = JobScheduler(self.config, self.run)
        scheduler.start()


def main():
    """Main function."""
    parser = argparse.ArgumentParser(
        description='AI Job Matcher - Find jobs that match your resume'
    )
    parser.add_argument(
        '--schedule',
        action='store_true',
        help='Run in scheduled mode (runs daily at configured time)'
    )
    parser.add_argument(
        '--once',
        action='store_true',
        help='Run once immediately and exit'
    )
    
    args = parser.parse_args()
    
    try:
        app = JobMatcherApp()
        
        if args.schedule:
            # Run in scheduled mode
            app.start_scheduler()
        else:
            # Run once
            app.run()
            
    except KeyboardInterrupt:
        logger.info("\n👋 Application stopped by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"❌ Fatal error: {str(e)}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
