import sys
sys.path.append(".")

from src.scrapers import scraper_dict  

from config.config_loader import ConfigLoader
loader = ConfigLoader()

def main(scrapers):

    yml = loader.load_yml()
    
    run_scrapers(scrapers, yml)

def run_scrapers(companies, config):
    scrapers = []

    for company in companies:
        # Check if the company has a scraper defined in the dictionary
        if company in scraper_dict:
            scraper_class = scraper_dict[company]  # Access the scraper class from the dictionary
            scraper_config = {**config['scrapers'][company]['config'], 'headers': config['headers']}  # Merge headers

            # Initialize the scraper with its specific config and universal headers
            scrapers.append(scraper_class(company,scraper_config))
            
        else:
            print(f"{company} scraper does not exist.")
    
    for scraper in scrapers:
        print(f"Running {scraper.scraper_name} job scraper...")
        scraper.scrape_job_urls()
        new_jobs = scraper.job_urls
        if new_jobs:
            print(f"Found {len(new_jobs)} new job(s) at {scraper.scraper_name}:")
            for job in new_jobs:
                print(f"URL: {job}")
                print(f"Info:",scraper.extract_job_page_content(job))
        else:
            print(f"No new jobs found for {scraper.scraper_name}.")

if __name__ == "__main__":
    scrapers = loader.get_available_scrapers()
    main(scrapers)
