# Job Finder LLM Project (In progress)

This project is for creating a database of job listings by using a modular webscraper on company websites. The current plan is to eventually use LangChain to read resumes and reccomend relevant jobs.
The list of compatible companies can be extended via YAML configuration.

## Features

- **Modular Design**: Easily add scrapers for new companies by editing the configuration and extending the base class.
- **Configurable Scraping**: Use YAML to define selectors and other parameters for each company's job listings.
- **Database-Ready**: Placeholder methods are included to store job data in a database if needed.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Contributing](#contributing)


## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/job-scraper.git
   cd job-scraper
   ```

2. **Set up a virtual environment (optional but recommended)**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. **Edit the YAML configuration**:
   The project uses a YAML file to configure the scraper for different companies. You can find and edit the configuration in the `config/scraper_config.yaml` file.

2. **Run the scraper**:
   The main script to run scrapers is `run_scrapers.py`. You can pass the company name as a command-line argument, or configure it in the YAML.
   
   Example:
   ```bash
   python scripts/run_scrapers.py --companies booz_allen
   ```

3. **Scraper Output**:
   The scraper prints job listings to the console, including job titles, locations, remote work information, and job URLs. It also supports placeholder methods to save job listings to a database.

## Configuration

The project is driven by a YAML configuration file located at `config/scraper_config.yaml`. This file defines:
- **Base URLs**: The starting points for scraping job listings.
- **CSS Selectors**: For extracting job titles, links, locations, and remote work details.
- **Pagination Controls**: Handles traversing paginated job listings.

### Example YAML Configuration

```yaml
booz_allen:
  base_url: "https://careers.boozallen.com"
  starting_urls:
    - "https://careers.boozallen.com/teams/digital/?..."
  tr_selector: "tr"  # Selector for table rows containing job listings
  td_job_title_class: "cell-title"  # Class for <td> containing job titles
  job_link_selector: "a.link"  # Selector for job links
  location_selector: "td[data-th='Location']"  # Selector for job location
  remote_work_selector: "td[data-th='Remote Work']"  # Selector for remote work details
  next_button_class: "list-controls__pagination__item paginationNextLink"  # Class for pagination controls
  headers:
    User-Agent: 'Mozilla/5.0'
```

## Adding a New Company

1. **Update the YAML Configuration**: Add a new entry in `scraper_config.yaml` for the new company.
2. **Create a Scraper Class**: Extend `BaseScraper` to handle the specific structure of the new company's job listings.
3. **Map the Scraper**: Add the new scraper to the `scrap_dict` in `run_scrapers.py`.

## Contributing

Contributions are welcome! If you find a bug or have a feature request, please open an issue or submit a pull request.

### Steps to Contribute

1. **Fork the repository**.
2. **Create a new branch**:
   ```bash
   git checkout -b feature-branch
   ```
3. **Make your changes**.
4. **Submit a pull request**.



### Next Steps

- Add database integration to store the scraped jobs.
- Add support for scraping more companies by extending the YAML configuration and creating new scraper classes.
- Set up automated tests to ensure consistent scraper behavior across different websites.
