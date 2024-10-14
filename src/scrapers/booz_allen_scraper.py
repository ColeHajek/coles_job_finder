from .base_scraper import BaseScraper
class BoozAllenScraper(BaseScraper):
    def __init__(self,name, config):
        """
        Initialize the Booz Allen scraper with specific config and universal headers.
        Pass the scraper name and config to the parent class (BaseScraper).
        """
        self.config = config
        super().__init__(name, config)

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
                #print(f"Found job URL: {job_url}")