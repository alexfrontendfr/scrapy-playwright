# Scrapy Playwright Web Scraper

<<<<<<< HEAD
This project uses Scrapy and Playwright to perform web scraping across various search engines, including Google, Bing, DuckDuckGo, and Tor .onion websites.

## Features

- Matrix-themed UI for search results.
- Supports scraping from Google, Bing, DuckDuckGo, and the dark web (.onion sites) using Tor.
- Real-time form validation with progress indicator.
- Adjustable search result limits.
- Fully responsive and modern tech-themed design.
- Proxy rotation and user-agent randomization.

## Setup Instructions

1. **Clone the repository**:

   git clone https://github.com/alexfrontendfr/scrapy-playwright.git

2. Navigate to the folder
   cd scrapy-playwright

3. Install dependencies

pip install -r requirements.txt

4. Set up playwright:
   playwright install
=======
This project uses Scrapy and Playwright to perform web scraping across various search engines, including Bing, DuckDuckGo, Google, and Tor .onion websites.

## Features

- Matrix-themed UI for search results
- Supports scraping from Bing, DuckDuckGo, Google, and .onion sites using Tor
- Real-time form validation with progress indicator
- Adjustable search result limits
- Proxy rotation and user-agent randomization
- Caching mechanism to store frequently accessed results

## Installation

Please refer to the SETUP_GUIDE.md file for detailed installation instructions.

## Running the Scraper

1. Activate your virtual environment (if you're using one).
2. Navigate to the project root directory.
3. Run the Flask application: cd scraper_bot/scraper_bot python app.py
4. Open your web browser and go to `http://127.0.0.1:5000/`
5. Enter your search term, select the search engine, set the result limit, and start scraping!

## How It Works

1. The Flask app (app.py) provides a web interface for users to input search terms and select options.
2. When a search is initiated, the app runs the appropriate spider (Bing, DuckDuckGo, Google, or Onion) using Scrapy and Playwright.
3. The spider navigates to the search engine, enters the query, and extracts the search results.
4. Results are cached to improve performance for repeated searches.
5. For .onion sites, the scraper uses Tor as a proxy to access the dark web.
6. The results are displayed in the web interface and can be downloaded in various formats.

## Customization

- To add new search engines, create a new spider in the `scraper_bot/spiders` directory following the pattern of existing spiders.
- Adjust proxy settings in `scraper_bot/settings.py` if you're using a proxy service.
- Modify the `PLAYWRIGHT_LAUNCH_OPTIONS` in `scraper_bot/settings.py` to change browser behavior.

## Troubleshooting

If you encounter any dependency conflicts, make sure you're using a virtual environment and that it's activated before installing dependencies or running the scraper.

## License

This project is licensed under the MIT License.
>>>>>>> 7b1b102 (Lots of updates for scraping)
