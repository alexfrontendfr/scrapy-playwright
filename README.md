# Web Scraper Setup Guide

## 1. Project Overview

This web scraper allows you to scrape search results from Bing, DuckDuckGo, and .onion sites. The project features:

- A Flask UI for inputting search terms, selecting search engines, and choosing output formats (JSON, CSV, SQLite).
- Automated scraping for multiple search terms and engines without overwriting results.
- Support for .onion scraping using Tor.

## 2. Cloning the Project from GitHub

To get started, clone the project from GitHub to your local machine:

```
git clone https://github.com/alexfrontendfr/scraper_bot.git
cd scraper_bot
```

## 3. Installation Commands

### For Windows:

1. Install Python: Download and install Python from [python.org](https://www.python.org/downloads/).
2. Install dependencies:

   ```
   pip install scrapy Flask scrapy-user-agents
   ```

3. Install Playwright for Scrapy:

   ```
   pip install scrapy-playwright
   playwright install
   ```

4. If you plan to scrape `.onion` sites, install **Tor**:
   - Download and install the **Tor Browser** from [torproject.org](https://www.torproject.org/download/).
   - Run **Tor** by executing:
   ```
   "C:\Program Files\Tor Browser\Browser\TorBrowser\Tor\tor.exe"
   ```

### For Linux:

1. Install Python if it's not already installed:

   ```
   sudo apt update
   sudo apt install python3 python3-pip
   ```

2. Install the required dependencies:

   ```
   pip3 install scrapy Flask scrapy-user-agents
   ```

3. Install Playwright for Scrapy:

   ```
   pip3 install scrapy-playwright
   playwright install
   ```

4. Install **Tor** for .onion scraping:

   ```
   sudo apt install tor
   ```

   Start Tor with:

   ```
   tor
   ```

## 4. Running the Flask UI

Once all dependencies are installed, start the Flask UI to begin scraping.

1. Navigate to the project directory:

   ```
   cd scraper_bot/scraper_bot
   ```

2. Run the Flask app:

   ```
   python app.py
   ```

3. Open your web browser and go to `http://127.0.0.1:5000/`.

4. You can now:
   - Input search terms.
   - Select the search engine (Bing, DuckDuckGo, or .onion).
   - Choose the output format (JSON, CSV, SQLite).
   - Start scraping!

## 5. Exporting Results

The scraper automatically saves results based on your selected format:

- **JSON**: Saved as `search_term_results.json`
- **CSV**: Saved as `search_term_results.csv`
- **SQLite**: Data is saved in an SQLite database.

## 6. Running Multiple Searches

The Flask app allows you to automate searches for different terms across multiple search engines, with outputs saved separately.

## 7. Scraping .Onion Sites

To scrape `.onion` sites:

1. Ensure **Tor** is running.
2. Choose `.onion` as the search engine from the Flask UI.
3. Enter a valid `.onion` URL as the search term or use a directory of `.onion` sites.

## 8. Additional Features and Customizations

You can expand the project to include more search engines by creating new spiders. For example, you can add a Google or Yahoo spider by following the same pattern used in `bing_spider.py` or `keyword_spider.py`.

If you encounter any issues or need further assistance, feel free to reach out!
