# Imports all the available scrapers into the scrapers namespace
from .booz_allen_scraper import BoozAllenScraper
# Add other scrapers as needed

# Dictionary for easy access
scraper_dict = {
    'booz_allen': BoozAllenScraper
    # Add other scrapers to the dictionary
}
