"""
Indeed job scraper for Germany.
"""

import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from scrapers.base_scraper import BaseScraper
from utils.logger import setup_logger

logger = setup_logger(__name__)


class IndeedScraper(BaseScraper):
    """Scraper for Indeed.de (Germany)."""
    
    def __init__(self, config):
        """Initialize Indeed scraper."""
        super().__init__(config, "Indeed.de")
        self.base_url = "https://de.indeed.com"
    
    def _build_search_url(self, job_title, location, page=0):
        """Build Indeed search URL."""
        # Indeed uses 'start' parameter for pagination (0, 10, 20, ...)
        start = page * 10
        
        job_query = job_title.replace(' ', '+')
        location_query = location.replace(' ', '+')
        
        url = f"{self.base_url}/jobs?q={job_query}&l={location_query}&start={start}&fromage=1"
        return url
    
    def scrape_jobs(self):
        """Scrape jobs from Indeed."""
        all_jobs = []
        driver = None
        
        try:
            driver = self._get_driver()
            
            for job_title in self.search_config['job_titles']:
                for location in self.search_config['locations']:
                    logger.info(f"  Searching: {job_title} in {location}")
                    
                    for page in range(self.max_pages):
                        try:
                            url = self._build_search_url(job_title, location, page)
                            driver.get(url)
                            self._delay()
                            
                            # Wait for job cards to load
                            WebDriverWait(driver, 10).until(
                                EC.presence_of_element_located((By.CLASS_NAME, "job_seen_beacon"))
                            )
                            
                            # Find job cards
                            job_cards = driver.find_elements(By.CLASS_NAME, "job_seen_beacon")
                            
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
            # Title
            title_elem = card.find_element(By.CSS_SELECTOR, "h2.jobTitle span")
            title = self._clean_text(title_elem.text)
            
            # Company
            try:
                company_elem = card.find_element(By.CSS_SELECTOR, "span[data-testid='company-name']")
                company = self._clean_text(company_elem.text)
            except NoSuchElementException:
                company = "Unknown"
            
            # Location
            try:
                location_elem = card.find_element(By.CSS_SELECTOR, "div[data-testid='text-location']")
                location = self._clean_text(location_elem.text)
            except NoSuchElementException:
                location = "Germany"
            
            # URL
            try:
                link_elem = card.find_element(By.CSS_SELECTOR, "h2.jobTitle a")
                job_url = link_elem.get_attribute('href')
                if not job_url.startswith('http'):
                    job_url = self.base_url + job_url
            except NoSuchElementException:
                return None
            
            # Salary (if available)
            salary = None
            try:
                salary_elem = card.find_element(By.CSS_SELECTOR, "div[data-testid='attribute_snippet_testid']")
                salary = self._clean_text(salary_elem.text)
            except NoSuchElementException:
                pass
            
            # Get full description (requires clicking)
            description = self._get_job_description(job_url, driver)
            
            job = {
                'title': title,
                'company': company,
                'location': location,
                'url': job_url,
                'description': description,
                'salary': salary,
                'posted_date': None,  # Indeed doesn't always show date
                'source': self.name
            }
            
            return job
            
        except Exception as e:
            logger.debug(f"    Error extracting job data: {e}")
            return None
    
    def _get_job_description(self, job_url, driver):
        """
        Get full job description by visiting job page.
        
        Args:
            job_url: Job URL
            driver: WebDriver instance
            
        Returns:
            Job description text
        """
        try:
            # Open in new tab
            driver.execute_script(f"window.open('{job_url}', '_blank');")
            driver.switch_to.window(driver.window_handles[-1])
            
            # Wait for description
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "jobDescriptionText"))
            )
            
            desc_elem = driver.find_element(By.ID, "jobDescriptionText")
            description = self._clean_text(desc_elem.text)
            
            # Close tab
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
            
            return description
            
        except Exception as e:
            logger.debug(f"    Could not get full description: {e}")
            # Close tab if opened
            if len(driver.window_handles) > 1:
                driver.close()
                driver.switch_to.window(driver.window_handles[0])
            return ""
