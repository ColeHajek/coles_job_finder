from .base_scraper import BaseScraper
import json
class BoozAllenScraper(BaseScraper):
    def __init__(self,name, config):
        """
        Initialize the Booz Allen scraper with specific config and universal headers.
        Pass the scraper name and config to the parent class (BaseScraper).
        """
        super().__init__(name, config)
        
        self.job_listing_class = config['job_listing_class']
        self.job_link_selector = config['job_link_selector']
        self.next_button_class = config['next_button_class']

    def extract_job_urls_from_page(self, url):

        """
        Override the base method to handle extracting job URLs from Booz Allen's specific HTML structure.
        """
        soup = self.send_request(url)
        
        # Find all <tr> elements
        all_rows = soup.find_all('tr')

        # Filter to only include <tr> elements that contain a <td class="cell-title">
        job_rows = [row for row in all_rows if row.find('td', class_='cell-title')]

        # Now, job_rows contains only the <tr> elements that have <td class="cell-title">
        for row in job_rows:
            job_title_cell = row.find('td', class_='cell-title')
            job_link_tag = job_title_cell.find('a', class_='link')

            if job_link_tag and 'href' in job_link_tag.attrs:

                job_url = self.ensure_full_url(job_link_tag['href'])
                self.job_urls.add(job_url)
                
    def extract_job_page_content(self, job_url):
        soup = self.send_request(job_url)
        job_details = {}
        # Extract data from a <script> tag containing JSON-LD for JobPosting
        script_tag = soup.find('script', text=lambda t: t and "JobPosting" in t)
        
        script_content = script_tag.string.strip()
        start_index = script_content.index("{")
        end_index = script_content.rindex("}") + 1
        json_data = json.loads(script_content[start_index:end_index])

        # Extract relevant fields from the JSON-LD
        job_details['title'] = json_data.get('title', 'Not found')
        job_details['description'] = json_data.get('description', 'Not found')
        job_details['date_posted'] = json_data.get('datePosted', 'Not found')
        job_details['city'] = json_data.get('jobLocation', {}).get('address', {}).get('addressLocality', 'Not found')
        job_details['state'] = json_data.get('jobLocation', {}).get('address', {}).get('addressRegion', 'Not found')
        
        # Add the date the data was scraped and the company name
        job_details['date_scraped'] = self.time_scraped
        job_details['company'] = self.scraper_name

        #print(job_details)
        return job_details

        
