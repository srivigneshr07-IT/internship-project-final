"""
Base Adapter - Abstract class for all source adapters
Defines the interface that all scrapers must implement
"""

from abc import ABC, abstractmethod
from typing import List
import requests
from bs4 import BeautifulSoup
import time
from etl.models import RawListing
from etl.config import SCRAPING_CONFIG
from etl.utils.logger import setup_logger

logger = setup_logger(__name__)


class BaseAdapter(ABC):
    """Abstract base class for source adapters"""
    
    def __init__(self, source_name: str, base_url: str, use_selenium: bool = False):
        self.source_name = source_name
        self.base_url = base_url
        self.use_selenium = use_selenium
        self.headers = {'User-Agent': SCRAPING_CONFIG['user_agent']}
        self.timeout = 10
        self.delay = SCRAPING_CONFIG['delay_between_requests']
        self._selenium_helper = None
    
    def fetch_html(self, url: str) -> str:
        """Fetch HTML from URL (uses Selenium if use_selenium=True)"""
        if self.use_selenium:
            return self.fetch_html_selenium(url)
        
        try:
            response = requests.get(url, headers=self.headers, timeout=self.timeout)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            logger.error(f"Failed to fetch {url}: {e}")
            return ""
    
    def fetch_html_selenium(self, url: str) -> str:
        """Fetch HTML using Selenium with auto-managed ChromeDriver"""
        try:
            from selenium import webdriver
            from selenium.webdriver.chrome.service import Service
            from selenium.webdriver.chrome.options import Options
            from selenium.webdriver.common.by import By
            from selenium.webdriver.support.ui import WebDriverWait
            from selenium.webdriver.support import expected_conditions as EC
            from webdriver_manager.chrome import ChromeDriverManager
            
            # Initialize driver if not exists
            if self._selenium_helper is None:
                options = Options()
                options.add_argument('--headless')
                options.add_argument('--no-sandbox')
                options.add_argument('--disable-dev-shm-usage')
                options.add_argument('--disable-gpu')
                options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
                
                service = Service(ChromeDriverManager().install())
                self._selenium_helper = webdriver.Chrome(service=service, options=options)
                logger.info("Selenium Chrome driver initialized with webdriver-manager")
            
            # Fetch page
            self._selenium_helper.get(url)
            
            # Wait for body
            WebDriverWait(self._selenium_helper, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            
            # Wait for dynamic content
            time.sleep(3)
            
            html = self._selenium_helper.page_source
            logger.info(f"Selenium fetched {len(html)} chars")
            
            return html
            
        except Exception as e:
            logger.error(f"Selenium fetch failed for {url}: {e}")
            if self._selenium_helper:
                try:
                    self._selenium_helper.quit()
                except:
                    pass
                self._selenium_helper = None
            return ""
    
    def __del__(self):
        """Cleanup Selenium driver"""
        if self._selenium_helper:
            try:
                self._selenium_helper.quit()
            except:
                pass
    
    def parse_html(self, html: str) -> BeautifulSoup:
        """Parse HTML into BeautifulSoup object"""
        return BeautifulSoup(html, 'lxml')
    
    @abstractmethod
    def scrape(self, city: str, max_pages: int = 3) -> List[RawListing]:
        """
        Scrape listings for a city
        Must be implemented by child classes
        """
        pass
    
    @abstractmethod
    def extract_listing(self, card) -> RawListing:
        """
        Extract data from a single listing card
        Must be implemented by child classes
        """
        pass
    
    def sleep(self):
        """Sleep between requests"""
        time.sleep(self.delay)
