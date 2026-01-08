"""
LinkedIn job scraper for Germany.
"""

import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from scrapers.base_scraper import BaseScraper
from utils.logger import setup_logger

logger = setup_logger(__name__)


class LinkedInScraper(BaseScraper):
    """Scraper for LinkedIn Jobs (Germany)."""
    
    def __init__(self, config):
        """Initialize LinkedIn scraper."""
        super().__init__(config, "LinkedIn")
        self.base_url = "https://www.linkedin.com"
        self.email = os.getenv('LINKEDIN_EMAIL')
        self.password = os.getenv('LINKEDIN_PASSWORD')
    
    def _build_search_url(self, job_title, location, page=0):
        """Build LinkedIn jobs search URL."""
        # LinkedIn uses 'start' parameter for pagination (0, 25, 50, ...)
        start = page * 25
        
        job_query = job_title.replace(' ', '%20')
        location_query = location.replace(' ', '%20')
        
        url = f"{self.base_url}/jobs/search/?keywords={job_query}&location={location_query}&f_TPR=r86400&start={start}"
        return url
    
    def _login(self, driver):
        """
        Login to LinkedIn (optional but recommended for better access).
        
        Args:
            driver: WebDriver instance
        """
        if not self.email or not self.password:
            logger.info("  LinkedIn credentials not provided, skipping login")
            return False
        
        try:
            driver.get(f"{self.base_url}/login")
            self._delay()
            
            # Enter email
            email_field = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "username"))
            )
            email_field.send_keys(self.email)
            
            # Enter password
            password_field = driver.find_element(By.ID, "password")
            password_field.send_keys(self.password)
            
            # Click login
            login_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
            login_button.click()
            
            # Wait for login to complete
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "global-nav"))
            )
            
            logger.info("  ✓ Logged in to LinkedIn")
            return True
            
        except Exception as e:
            logger.warning(f"  Failed to login to LinkedIn: {e}")
            return False
    
    def scrape_jobs(self):
        """Scrape jobs from LinkedIn."""
        all_jobs = []
        driver = None
        
        try:
            driver = self._get_driver()
            
            # Try to login (optional)
            self._login(driver)
            
            for job_title in self.search_config['job_titles']:
                for location in self.search_config['locations']:
                    logger.info(f"  Searching: {job_title} in {location}")
                    
                    for page in range(self.max_pages):
                        try:
                            url = self._build_search_url(job_title, location, page)
                            driver.get(url)
                            self._delay()
                            
                            # Wait for job cards
                            WebDriverWait(driver, 10).until(
                                EC.presence_of_element_located((By.CLASS_NAME, "jobs-search__results-list"))
                            )
                            
                            # Find job cards
                            job_cards = driver.find_elements(By.CSS_SELECTOR, "li.jobs-search-results__list-item")
                            
                            if not job_cards:
                                logger.info(f"    No more jobs found on page {page+1}")
                                break
                            
                            logger.info(f"    Page {page+1}: Found {len(job_cards)} jobs")
                            
                            for card in job_cards:
                                try:
                                    job = self._extract_job_data(card, driver)
                                    if job:
                                        all_jobs.append(job)
                                except Exception as e:
                                    logger.debug(f"    Error extracting job: {e}")
                                    continue
                            
                        except TimeoutException:
                            logger.warning(f"    Timeout on page {page+1}")
                            break
                        except Exception as e:
                            logger.error(f"    Error on page {page+1}: {e}")
                            break
                    
                    self._delay()
            
        finally:
            if driver:
                driver.quit()
        
        return all_jobs
    
    def _extract_job_data(self, card, driver):
        """Extract job data from a job card."""
        try:
            # Click on job card to load details
            card.click()
            self._delay()
            
            # Title
            title_elem = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "h2.job-details-jobs-unified-top-card__job-title"))
            )
            title = self._clean_text(title_elem.text)
            
            # Company
            try:
                company_elem = driver.find_element(By.CSS_SELECTOR, "a.job-details-jobs-unified-top-card__company-name")
                company = self._clean_text(company_elem.text)
            except NoSuchElementException:
                company = "Unknown"
            
            # Location
            try:
                location_elem = driver.find_element(By.CSS_SELECTOR, "span.job-details-jobs-unified-top-card__bullet")
                location = self._clean_text(location_elem.text)
            except NoSuchElementException:
                location = "Germany"
            
            # URL
            job_url = driver.current_url
            
            # Description
            try:
                desc_elem = driver.find_element(By.CSS_SELECTOR, "div.jobs-description-content__text")
                description = self._clean_text(desc_elem.text)
            except NoSuchElementException:
                description = ""
            
            # Salary (if available)
            salary = None
            try:
                salary_elem = driver.find_element(By.CSS_SELECTOR, "span.job-details-jobs-unified-top-card__job-insight")
                salary = self._clean_text(salary_elem.text)
            except NoSuchElementException:
                pass
            
            job = {
                'title': title,
                'company': company,
                'location': location,
                'url': job_url,
                'description': description,
                'salary': salary,
                'posted_date': None,
                'source': self.name
            }
            
            return job
            
        except Exception as e:
            logger.debug(f"    Error extracting job data: {e}")
            return None
