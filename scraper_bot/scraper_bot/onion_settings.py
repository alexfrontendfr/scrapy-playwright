# Scrapy settings for onion_scraping project
BOT_NAME = 'onion_scraper'
SPIDER_MODULES = ['scraper_bot.spiders']
NEWSPIDER_MODULE = 'scraper_bot.spiders'

# Use Tor for `.onion` scraping
DOWNLOADER_MIDDLEWARES = {
    'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 1,
}

# Set Tor proxy
HTTP_PROXY = 'socks5://127.0.0.1:9050'

# Enable retries
RETRY_ENABLED = True
RETRY_TIMES = 5

# Download delay to avoid being blocked
DOWNLOAD_DELAY = 3
