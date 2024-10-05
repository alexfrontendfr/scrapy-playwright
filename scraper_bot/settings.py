import os

BOT_NAME = 'matrix_web_scraper'

SPIDER_MODULES = ['scraper_bot.spiders']
NEWSPIDER_MODULE = 'scraper_bot.spiders'

ROBOTSTXT_OBEY = True
CONCURRENT_REQUESTS = 32
DOWNLOAD_DELAY = 0.5
RANDOMIZE_DOWNLOAD_DELAY = True

AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 5
AUTOTHROTTLE_MAX_DELAY = 60
AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0

HTTPCACHE_ENABLED = True
HTTPCACHE_EXPIRATION_SECS = 0
HTTPCACHE_DIR = 'httpcache'
HTTPCACHE_IGNORE_HTTP_CODES = []
HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

DOWNLOAD_HANDLERS = {
    "http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
    "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
}

TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"

PLAYWRIGHT_LAUNCH_OPTIONS = {
    "headless": True,
    "timeout": 20 * 1000,
    "proxy": {
        "server": "socks5://127.0.0.1:9050"
    }
}

SEARCH_CACHE_DIR = 'search_cache'
SEARCH_CACHE_DURATION = 86400  # 24 hours

DOWNLOADER_MIDDLEWARES = {
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
    'scraper_bot.middlewares.RandomUserAgentMiddleware': 400,
    'scraper_bot.middlewares.ProxyMiddleware': 350,
    'scrapy_playwright.middleware.PlaywrightMiddleware': 1000,
}

ITEM_PIPELINES = {
    'scraper_bot.pipelines.WebScraperPipeline': 300,
}

LOG_LEVEL = 'INFO'
LOG_FILE = 'scraper.log'

RETRY_ENABLED = True
RETRY_TIMES = 3
RETRY_HTTP_CODES = [500, 502, 503, 504, 522, 524, 408, 429]

DATABASE_URL = os.environ.get('DATABASE_URL', 'sqlite:///scraper_results.db')

TOR_PROXY = 'socks5://127.0.0.1:9050'
TOR_CONTROL_PORT = 9051
TOR_PASSWORD = os.environ.get('TOR_PASSWORD', '')

USER_AGENT_LIST = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Safari/605.1.15',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36',
]

DNS_SERVERS = ['127.0.0.1']