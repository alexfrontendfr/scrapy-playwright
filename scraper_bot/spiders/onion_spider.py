import scrapy
from scrapy_playwright.page import PageCoroutine
from scraper_bot.utils.proxy_helper import tor_manager, get_tor_proxy
from scraper_bot.utils.cache_manager import cache_manager
import json

class OnionSpider(scrapy.Spider):
    name = "onion_spider"
    allowed_domains = [".onion"]
    
    def __init__(self, query=None, limit=50, *args, **kwargs):
        super(OnionSpider, self).__init__(*args, **kwargs)
        self.query = query
        self.limit = int(limit)
        self.result_count = 0
        self.results = []

    start_urls = [
        "http://msydqstlz2kzerdg.onion",  # Ahmia search engine
        "http://hss3uro2hsxfogfq.onion",  # Torch search engine
        "http://xmh57jrzrnw6insl.onion",  # DuckDuckGo for .onion
        "http://grams7enufi7jmdl.onion",  # Grams search engine
        "http://torlinkbgs6aabns.onion",  # TorLinks directory
        "http://deepwebwikiidwd.onion"    # Deep Web Wiki
    ]

    custom_settings = {
        "PLAYWRIGHT_LAUNCH_OPTIONS": {
            "headless": True,
            "args": ["--proxy-server=socks5://127.0.0.1:9050"]  # Using Tor for .onion scraping
        },
        "RETRY_ENABLED": True,
        "RETRY_TIMES": 5,  # Retry up to 5 times for failed requests
        "DOWNLOAD_TIMEOUT": 30
    }

    def start_requests(self):
        cached_results = cache_manager.get_cached_results(self.query, 'onion')
        if cached_results:
            self.logger.info(f"Using cached results for query: {self.query}")
            for result in cached_results:
                yield result
            return

        for url in self.start_urls:
            yield scrapy.Request(
                url=f"{url}/search?q={self.query}",
                meta={
                    'playwright': True,
                    'playwright_page_coroutines': [
                        PageCoroutine('wait_for_selector', '.result-title a')
                    ]
                },
                callback=self.parse_results
            )

    def parse_results(self, response):
        results = response.css('.result')
        for idx, result in enumerate(results):
            if self.result_count < self.limit:
                title = result.css('.result-title a::text').get()
                link = result.css('.result-title a::attr(href)').get()
                item = {'title': title, 'url': link}
                self.results.append(item)
                self.result_count += 1
                yield item
            else:
                break

        if self.result_count < self.limit:
            next_page = response.css('a.pagination-next::attr(href)').get()
            if next_page:
                next_page_url = response.urljoin(next_page)
                yield scrapy.Request(
                    url=next_page_url,
                    meta={'playwright': True},
                    callback=self.parse_results
                )
        else:
            cache_manager.cache_results(self.query, 'onion', self.results)

    def closed(self, reason):
        with open('output.json', 'w') as f:
            json.dump(self.results, f, indent=4)