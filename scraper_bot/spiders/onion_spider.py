import scrapy
from scraper_bot.spiders.base_spider import BaseSpider
from scrapy_playwright.page import PageMethod
from scraper_bot.utils.cache_manager import cache_manager
from scraper_bot.utils.tor_manager import renew_tor_ip, get_tor_proxy
import json
from urllib.parse import urljoin
import time

class OnionSpider(BaseSpider):
    name = "onion_spider"
    allowed_domains = [".onion"]

    start_urls = [
        "http://xmh57jrzrnw6insl.onion",  # DuckDuckGo .onion
        "http://zqktlwiuavvvqqt4ybvgvi7tyo4hjl5xgfuvpdf6otjiycgwqbym2qad.onion",  # Torch
        "http://juhanurmihxlp77nkq76byazcldy2hlmovfu2epvl5ankdibsot4csyd.onion",  # Ahmia
        "http://haystak5njsmn2hqkewecpaxetahtwhsbsa64jom2k22z5afxhnpxfid.onion",  # Haystak
        "http://gjobqjj7wyczbqie.onion",  # Candle
    ]

    custom_settings = {
        "PLAYWRIGHT_LAUNCH_OPTIONS": {
            "headless": True,
            "proxy": {
                "server": get_tor_proxy()
            }
        },
        "RETRY_ENABLED": True,
        "RETRY_TIMES": 5,
        "DOWNLOAD_TIMEOUT": 60,
        "ROBOTSTXT_OBEY": False,
    }

    def __init__(self, query=None, limit=10, *args, **kwargs):
        super().__init__(query, limit, *args, **kwargs)
        self.use_tor = True

    def start_requests(self):
        cached_results = cache_manager.get_cached_results(self.query, 'onion')
        if cached_results:
            self.logger.info(f"Using cached results for query: {self.query}")
            for result in cached_results[:self.limit]:
                yield self.process_result(result)
            return

        for url in self.start_urls:
            yield scrapy.Request(
                url=f"{url}/search?q={self.query}",
                meta={
                    'playwright': True,
                    'playwright_page_methods': [
                        PageMethod('wait_for_selector', '.result-link', timeout=30000),
                    ]
                },
                callback=self.parse_results,
                errback=self.errback_httpbin,
            )

    def parse_results(self, response):
        for result in response.css('.result'):
            if self.results_fetched >= self.limit:
                return
            title = result.css('.result-link::text').get()
            link = result.css('.result-link::attr(href)').get()
            snippet = result.css('.result-snippet::text').get()
            yield self.process_result({'title': title, 'url': link, 'snippet': snippet})

        if self.results_fetched < self.limit:
            next_page = response.css('a.next::attr(href)').get()
            if next_page:
                renew_tor_ip()
                yield scrapy.Request(
                    url=urljoin(response.url, next_page),
                    meta={'playwright': True},
                    callback=self.parse_results,
                    errback=self.errback_httpbin,
                )
        else:
            cache_manager.cache_results(self.query, 'onion', self.results)

    def errback_httpbin(self, failure):
        self.logger.error(f"Error occurred: {failure}")
        if failure.check(scrapy.exceptions.IgnoreRequest):
            return
        renew_tor_ip()
        request = failure.request.copy()
        request.dont_filter = True
        yield request