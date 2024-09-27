# Scrapy settings for the project
BOT_NAME = 'scrapy_playwright'

SPIDER_MODULES = ['scraper_bot.spiders']
NEWSPIDER_MODULE = 'scraper_bot.spiders'

# Playwright integration settings
DOWNLOAD_HANDLERS = {
    "http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
    "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
}

# Enable Playwright
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"

# Custom middlewares
DOWNLOADER_MIDDLEWARES = {
    'scraper_bot.middlewares.RandomUserAgentMiddleware': 400,
    'scraper_bot.middlewares.ProxyMiddleware': 410,
}

# Enable AutoThrottle to avoid overloading servers
AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 5
AUTOTHROTTLE_MAX_DELAY = 60
AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0

# Retry failed requests
RETRY_ENABLED = True
RETRY_TIMES = 3  # Retries failed requests up to 3 times
RETRY_HTTP_CODES = [500, 502, 503, 504, 522, 524, 408, 429]

# Timeouts and delays for more sophisticated scraping
DOWNLOAD_TIMEOUT = 30  # 30 seconds timeout
DOWNLOAD_DELAY = 2  # Wait 2 seconds between requests

# Randomize download delay to prevent pattern detection
RANDOMIZE_DOWNLOAD_DELAY = True

# Logging settings for better debugging
LOG_LEVEL = 'INFO'

# ScraperAPI proxy integration (you can replace the key with your actual key)
HTTP_PROXY = 'http://53c1928a053353099bf02d77dec3a45b@scraperapi.com:8001'

# User agents
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36"
]

# ScraperAPI replaces the previous proxies
PROXIES = [
    HTTP_PROXY
]

# No proxy authentication needed for ScraperAPI
PROXY_AUTH = None
