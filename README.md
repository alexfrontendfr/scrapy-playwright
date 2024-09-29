# Matrix Web Scraper

A powerful and stylish web scraper with a Matrix-inspired UI, capable of scraping various search engines including Google, Bing, DuckDuckGo, and Onion sites.

## Features

- Matrix-themed UI for an immersive experience
- Support for multiple search engines (Google, Bing, DuckDuckGo, Onion)
- Tor integration for anonymous scraping
- Celery task queue for efficient background processing
- Caching mechanism to store frequently accessed results
- Real-time progress tracking
- Downloadable results in JSON format
- Proxy rotation and user-agent randomization
- Respect for robots.txt and ethical scraping practices

## Installation

1. Clone the repository:

   ```
   git clone https://github.com/yourusername/matrix-web-scraper.git
   cd matrix-web-scraper
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

5. Install and start Redis (required for Celery):
   - On Ubuntu: `sudo apt-get install redis-server`
   - On macOS: `brew install redis`
   - On Windows: Download and install from https://redis.io/download

## Running the Application

1. Start the Redis server (if not already running):

   ```
   redis-server
   ```

2. Start the Celery worker:

   ```
   celery -A scraper_bot.tasks worker --loglevel=info
   ```

3. Run the Flask application:

   ```
   python scraper_bot/app.py
   ```

4. Open your web browser and navigate to `http://localhost:5000`

## Usage

1. Enter your search query
2. Select the desired search engine(s)
3. Set the result limit
4. Choose whether to use Tor for anonymous scraping
5. Click "Start Search" and wait for the results

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License. See the LICENSE file for details.
