import re
import requests
from bs4 import BeautifulSoup
from datetime import datetime

class BaseScraper:
    def __init__(self, scraper_name, config):
        """
        Base Scraper constructor that initializes common scraper attributes.
        The child scrapers will pass their specific 'scraper_name' and 'config'.
        """
        self.scraper_name = scraper_name
        
        self.url_reconstructor = config['base_url']
        self.headers = config['headers']
        self.starting_urls = config['starting_urls']
        self.config = config
        self.job_urls = set()
        self.time_scraped = datetime.now().strftime('%Y-%m-%d')

    def send_request(self, url):
        """
        Sends an HTTP request with the provided headers and returns a BeautifulSoup object.
        """
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            return BeautifulSoup(response.text, 'html.parser')
        else:
            raise Exception(f"Failed to retrieve page: {url}, Status Code: {response.status_code}")

    def store_jobs_in_db(self):
        """
        Placeholder method for storing jobs in the database.
        """
        pass

    def scrape_job_urls(self):
        """
        For each starting link of job pages append any job urls found and continue
        to the next job page from the starting link
        """
        visited_urls = set()
        
        for start_url in self.starting_urls:
            current_url = start_url
            
            while current_url and current_url not in visited_urls:
                print(f"Visiting: {current_url}")
                visited_urls.add(current_url)

                # Send HTTP request and parse the HTML response
                soup = self.send_request(current_url)
                
                # Extract job URLs from the page
                self.extract_job_urls_from_page(current_url)
                
                # Get the next page URL for pagination
                current_url = self.get_next_page_url(soup)
        
    def get_next_page_url(self, soup):
        """
        Finds and returns the URL of the next page in the pagination, if available.
        """
        next_button = soup.find('a', class_=self.next_button_class)
        if next_button and 'href' in next_button.attrs:
            return next_button['href']
        else:
            return None
    
    def extract_job_urls_from_page(self, url):
        """
        Extract job URLs from the current page's HTML and add them to the job_listings set.
        """
        soup = self.send_request(url)
        job_items = soup.find_all('div', class_=self.job_listing_class)
        for item in job_items:
            job_link = item.find(self.job_link_selector)

            if job_link and 'href' in job_link.attrs:
                job_url = self.ensure_full_url(job_link['href'])
                self.extract_job_page_content(job_url)
                self.job_urls.add(job_url)
                print(f"Found job URL: {job_url}")
                       
    def ensure_full_url(self, relative_url):
        """
        Constructs a full URL from a relative URL if needed.
        """
        return relative_url if relative_url.startswith("http") else f"{self.base_url}{relative_url}"
    
    def extract_job_page_content(self, job_url):
        """Exctracts content of """
        return
        