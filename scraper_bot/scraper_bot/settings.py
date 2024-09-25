# Scrapy settings for scraper_bot project
BOT_NAME = 'scraper_bot'

SPIDER_MODULES = ['scraper_bot.spiders']
NEWSPIDER_MODULE = 'scraper_bot.spiders'

# ScraperAPI proxy service for rotating proxies
DOWNLOADER_MIDDLEWARES = {
    'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 1,
}

# Add your ScraperAPI key here
HTTP_PROXY = 'http://53c1928a053353099bf02d77dec3a45b@scraperapi.com:8001'

# Enable retries
RETRY_ENABLED = True
RETRY_TIMES = 5

# Download delay to avoid CAPTCHAs
DOWNLOAD_DELAY = 2
RANDOMIZE_DOWNLOAD_DELAY = True

# Rotate user agents to mimic different browsers
USER_AGENT_LIST = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36',
]

DOWNLOADER_MIDDLEWARES.update({
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
    'scrapy_user_agents.middlewares.RandomUserAgentMiddleware': 400,
})

ROBOTSTXT_OBEY = False  # Disable robots.txt to scrape more freely
LOG_ENABLED = True
LOG_LEVEL = 'INFO'

# Export feed format
FEED_FORMAT = 'json'
FEED_URI = 'output.json'
