
# Scrapy Playwright Web Scraper

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

   git clone https://github.com/yourusername/scrapy-playwright.git

2. **Navigate to the project directory**:

   cd scrapy-playwright

3. **Install the required dependencies**:

   pip install -r requirements.txt

4. **Set up Playwright** (required for headless browser interaction):

   playwright install

5. **Install Tor** (for .onion scraping):

   If you wish to scrape .onion sites, make sure Tor is installed and configured. You can download it from [Tor Project](https://www.torproject.org/download/).

6. **Configure ScraperAPI**:

   Replace the ScraperAPI key in `settings.py`:

   HTTP_PROXY = 'http://YOUR_SCRAPERAPI_KEY@scraperapi.com:8001'

7. **Run the Scraper**:

   Use the following command to run the scraper with a specific spider:

   scrapy crawl <spider_name>

   Available spiders:
   - `google_spider`: for Google searches.
   - `bing_spider`: for Bing searches.
   - `keyword_spider`: for DuckDuckGo searches.
   - `onion_spider`: for .onion site scraping using Tor.

8. **View Results**:

   Once the scraper is complete, you can view the results on the web interface by visiting `http://localhost:5000` (if using Flask).

## License

This project is licensed under the MIT License.
