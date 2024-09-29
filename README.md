# Scrapy Playwright Web Scraper

This project uses Scrapy and Playwright to perform web scraping across various search engines, including Google, Bing, DuckDuckGo, and Tor .onion websites.

## Features

- Matrix-themed UI for search results
- Supports scraping from Google, Bing, DuckDuckGo, and the dark web (.onion sites) using Tor
- Real-time progress tracking with progress indicator
- Adjustable search result limits
- Fully responsive and modern tech-themed design
- Proxy rotation and user-agent randomization
- Caching mechanism to store frequently accessed results
- Respect for robots.txt and ethical scraping practices

## Installation

1. Clone the repository:

   ```
   git clone https://github.com/alexfrontendfr/scrapy-playwright.git
   cd scrapy-playwright
   ```

2. Create and activate a virtual environment:

   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the required dependencies:

   ```
   pip install -r requirements.txt
   ```

4. Install Playwright browsers:

   ```
   playwright install
   ```

5. Install Tor (for .onion scraping):
   - Windows: Download and install the Tor Browser from https://www.torproject.org/download/
   - macOS: `brew install tor`
   - Linux: `sudo apt install tor`

## Running the Scraper

1. Activate your virtual environment (if not already activated)
2. Navigate to the project root directory
3. Run the Flask application:
   ```
   python scraper_bot/app.py
   ```
4. Open your web browser and go to `http://127.0.0.1:5000/`
5. Enter your search term, select the search engine, set the result limit, and start scraping!

## Configuration

- Adjust scraping settings in `scraper_bot/settings.py`
- Modify spider behavior in `scraper_bot/spiders/`
- Update caching settings in `scraper_bot/utils/cache_manager.py`

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License.
