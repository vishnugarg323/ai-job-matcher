"""
Job scheduler for running job matching every 30 minutes.
"""

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.interval import IntervalTrigger
import pytz
from utils.logger import setup_logger

logger = setup_logger(__name__)


class JobScheduler:
    """Schedule job matching runs every 30 minutes."""
    
    def __init__(self, config, job_function):
        """
        Initialize job scheduler.
        
        Args:
            config: Application configuration
            job_function: Function to run on schedule
        """
        self.config = config
        self.job_function = job_function
        self.scheduler = BlockingScheduler()
        
        # Get schedule settings
        schedule_config = config['schedule']
        self.enabled = schedule_config['enabled']
        self.interval_minutes = schedule_config.get('interval_minutes', 30)
        self.timezone = pytz.timezone(schedule_config['timezone'])
    
    def start(self):
        """Start the scheduler."""
        if not self.enabled:
            logger.warning("Scheduler is disabled in configuration")
            return
        
        # Create interval trigger - run every X minutes
        trigger = IntervalTrigger(
            minutes=self.interval_minutes,
            timezone=self.timezone
        )
        
        # Add job
        self.scheduler.add_job(
            self.job_function,
            trigger=trigger,
            id='job_matcher',
            name='AI Job Matcher',
            replace_existing=True
        )
        
        logger.info(f"⏰ Scheduler started - Will run every {self.interval_minutes} minutes ({self.timezone})")
        logger.info(f"🚨 URGENT MODE: Maximum job search frequency for visa deadline!")
        logger.info("Press Ctrl+C to stop")
        
        # Run immediately on start
        logger.info("🎯 Running first scan now...")
        self.job_function()
        
        try:
            self.scheduler.start()
        except (KeyboardInterrupt, SystemExit):
            logger.info("Scheduler stopped")
            self.scheduler.shutdown()
