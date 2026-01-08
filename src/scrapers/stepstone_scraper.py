"""
StepStone job scraper for Germany.
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from scrapers.base_scraper import BaseScraper
from utils.logger import setup_logger

logger = setup_logger(__name__)


class StepStoneScraper(BaseScraper):
    """Scraper for StepStone.de (Germany)."""
    
    def __init__(self, config):
        """Initialize StepStone scraper."""
        super().__init__(config, "StepStone.de")
        self.base_url = "https://www.stepstone.de"
    
    def _build_search_url(self, job_title, location, page=1):
        """Build StepStone search URL."""
        job_query = job_title.replace(' ', '-')
        location_query = location.replace(' ', '-')
        
        url = f"{self.base_url}/jobs/{job_query}/in-{location_query}?page={page}&radius=30"
        return url
    
    def scrape_jobs(self):
        """Scrape jobs from StepStone."""
        all_jobs = []
        driver = None
        
        try:
            driver = self._get_driver()
            
            for job_title in self.search_config['job_titles']:
                for location in self.search_config['locations']:
                    logger.info(f"  Searching: {job_title} in {location}")
                    
                    for page in range(1, self.max_pages + 1):
                        try:
                            url = self._build_search_url(job_title, location, page)
                            driver.get(url)
                            self._delay()
                            
                            # Accept cookies if present
                            try:
                                cookie_btn = WebDriverWait(driver, 5).until(
                                    EC.element_to_be_clickable((By.ID, "ccmgt_explicit_accept"))
                                )
                                cookie_btn.click()
                            except:
                                pass
                            
                            # Wait for job listings
                            WebDriverWait(driver, 10).until(
                                EC.presence_of_element_located((By.CSS_SELECTOR, "article[data-at='job-item']"))
                            )
                            
                            # Find job cards
                            job_cards = driver.find_elements(By.CSS_SELECTOR, "article[data-at='job-item']")
                            
                            if not job_cards:
                                logger.info(f"    No more jobs found on page {page}")
                                break
                            
                            logger.info(f"    Page {page}: Found {len(job_cards)} jobs")
                            
                            for card in job_cards:
                                try:
                                    job = self._extract_job_data(card)
                                    if job:
                                        all_jobs.append(job)
                                except Exception as e:
                                    logger.debug(f"    Error extracting job: {e}")
                                    continue
                            
                        except TimeoutException:
                            logger.warning(f"    Timeout on page {page}")
                            break
                        except Exception as e:
                            logger.error(f"    Error on page {page}: {e}")
                            break
                    
                    self._delay()
            
        finally:
            if driver:
                driver.quit()
        
        return all_jobs
    
    def _extract_job_data(self, card):
        """Extract job data from a job card."""
        try:
            # Title
            title_elem = card.find_element(By.CSS_SELECTOR, "h2[data-at='job-item-title'] a")
            title = self._clean_text(title_elem.text)
            
            # URL
            job_url = title_elem.get_attribute('href')
            
            # Company
            try:
                company_elem = card.find_element(By.CSS_SELECTOR, "div[data-at='job-item-company-name']")
                company = self._clean_text(company_elem.text)
            except NoSuchElementException:
                company = "Unknown"
            
            # Location
            try:
                location_elem = card.find_element(By.CSS_SELECTOR, "span[data-at='job-item-location']")
                location = self._clean_text(location_elem.text)
            except NoSuchElementException:
                location = "Germany"
            
            # Description snippet
            try:
                desc_elem = card.find_element(By.CSS_SELECTOR, "div[data-at='job-item-teaser']")
                description = self._clean_text(desc_elem.text)
            except NoSuchElementException:
                description = ""
            
            # Salary (if available)
            salary = None
            try:
                salary_elem = card.find_element(By.CSS_SELECTOR, "span[data-at='job-item-salary-info']")
                salary = self._clean_text(salary_elem.text)
            except NoSuchElementException:
                pass
            
            job = {
                'title': title,
                'company': company,
                'location': location,
                'url': job_url,
                'description': description,  # Note: This is just a snippet
                'salary': salary,
                'posted_date': None,
                'source': self.name
            }
            
            return job
            
        except Exception as e:
            logger.debug(f"    Error extracting job data: {e}")
            return None
