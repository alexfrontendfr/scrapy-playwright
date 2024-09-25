# Scrapy settings
BOT_NAME = 'scraper_bot'
SPIDER_MODULES = ['spiders']
NEWSPIDER_MODULE = 'spiders'

# Enable the ScraperAPI proxy service
DOWNLOADER_MIDDLEWARES = {
    'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 1,
}

# Your ScraperAPI key
HTTP_PROXY = 'http://53c1928a053353099bf02d77dec3a45b@scraperapi.com:8001'

# Enable retries
RETRY_ENABLED = True
RETRY_TIMES = 10

# Download delay to avoid CAPTCHAs
DOWNLOAD_DELAY = 2
RANDOMIZE_DOWNLOAD_DELAY = True

# Rotate User Agents to mimic different browsers
USER_AGENT_LIST = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36',
    # Add more user agents
]

DOWNLOADER_MIDDLEWARES.update({
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
    'scrapy_user_agents.middlewares.RandomUserAgentMiddleware': 400,
})


LOG_ENABLED = True
LOG_LEVEL = 'INFO'  # Change to 'ERROR' for minimal logging


