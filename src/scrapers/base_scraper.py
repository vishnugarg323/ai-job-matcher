"""
Base scraper class for job portals.
"""

import time
import random
from abc import ABC, abstractmethod
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from utils.logger import setup_logger

logger = setup_logger(__name__)


class BaseScraper(ABC):
    """Base class for all job scrapers."""
    
    def __init__(self, config, name):
        """
        Initialize base scraper.
        
        Args:
            config: Application configuration
            name: Scraper name
        """
        self.config = config
        self.name = name
        self.scraping_config = config['scraping']
        self.search_config = config['search']
        self.max_pages = self.scraping_config['max_pages']
        self.request_delay = self.scraping_config['request_delay']
        
    def _get_driver(self):
        """
        Get Selenium WebDriver with options.
        
        Returns:
            WebDriver instance
        """
        options = Options()
        
        if self.scraping_config['headless']:
            options.add_argument('--headless')
        
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        
        # Random user agent
        user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        ]
        
        if self.scraping_config['rotate_user_agent']:
            options.add_argument(f'user-agent={random.choice(user_agents)}')
        
        # Use ChromeDriverManager to automatically manage driver
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        driver.set_page_load_timeout(self.scraping_config['timeout'])
        
        return driver
    
    def _delay(self):
        """Add random delay between requests."""
        delay = self.request_delay + random.uniform(0, 1)
        time.sleep(delay)
    
    def _build_search_url(self, job_title, location, page=0):
        """
        Build search URL for the portal.
        
        Args:
            job_title: Job title to search
            location: Location to search
            page: Page number
            
        Returns:
            Search URL
        """
        # To be implemented by subclasses
        raise NotImplementedError
    
    @abstractmethod
    def scrape_jobs(self):
        """
        Scrape jobs from the portal.
        
        Returns:
            List of job dictionaries
        """
        pass
    
    def _clean_text(self, text):
        """
        Clean scraped text.
        
        Args:
            text: Text to clean
            
        Returns:
            Cleaned text
        """
        if not text:
            return ""
        
        # Remove extra whitespace
        text = ' '.join(text.split())
        return text.strip()
