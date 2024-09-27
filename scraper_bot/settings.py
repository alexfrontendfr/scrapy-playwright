# Scrapy settings for scraper_bot project

BOT_NAME = 'scraper_bot'

SPIDER_MODULES = ['scraper_bot.spiders']
NEWSPIDER_MODULE = 'scraper_bot.spiders'

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# Configure maximum concurrent requests performed by Scrapy
CONCURRENT_REQUESTS = 16

# Configure a delay for requests for the same website
DOWNLOAD_DELAY = 3

# Enable or disable downloader middlewares
DOWNLOADER_MIDDLEWARES = {
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
    'scrapy_user_agents.middlewares.RandomUserAgentMiddleware': 400,
    'scrapy_playwright.middleware.PlaywrightMiddleware': 1000,
}

# Enable or disable extensions
EXTENSIONS = {
    'scrapy.extensions.telnet.TelnetConsole': None,
}

# Configure item pipelines
ITEM_PIPELINES = {
    'scraper_bot.pipelines.ScraperBotPipeline': 300,
}

# Enable and configure the AutoThrottle extension
AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 5
AUTOTHROTTLE_MAX_DELAY = 60
AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
AUTOTHROTTLE_DEBUG = False

# Enable showing throttling stats for every response received
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching
HTTPCACHE_ENABLED = True
HTTPCACHE_EXPIRATION_SECS = 0
HTTPCACHE_DIR = 'httpcache'
HTTPCACHE_IGNORE_HTTP_CODES = []
HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

# Playwright settings
DOWNLOAD_HANDLERS = {
    "http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
    "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
}

TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"

PLAYWRIGHT_LAUNCH_OPTIONS = {
    "headless": True,
    "timeout": 20 * 1000,  # 20 seconds
}

# Custom settings
SEARCH_CACHE_DIR = 'search_cache'
SEARCH_CACHE_DURATION = 86400  # 24 hours