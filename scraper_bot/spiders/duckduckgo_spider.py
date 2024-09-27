import scrapy
from scrapy_playwright.page import PageCoroutine
import random
import json
from scraper_bot.utils.proxy_helper import proxy_manager, tor_manager, get_tor_proxy
from scraper_bot.utils.cache_manager import cache_manager

class DuckDuckGoSpider(scrapy.Spider):
    name = "duckduckgo_spider"
    
    def __init__(self, query=None, limit=50, use_tor=False, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.query = query
        self.limit = int(limit)
        self.results_fetched = 0
        self.use_tor = use_tor
        self.results = []

    def start_requests(self):
        cached_results = cache_manager.get_cached_results(self.query, 'duckduckgo')
        if cached_results:
            self.logger.info(f"Using cached results for query: {self.query}")
            for result in cached_results:
                yield result
            return

        url = f"https://duckduckgo.com/?q={self.query}"
        
        if self.use_tor:
            proxy = get_tor_proxy()
            tor_manager.renew_tor_ip()
        else:
            proxy = proxy_manager.get_random_proxy()

        yield scrapy.Request(
            url=url,
            meta={
                'playwright': True,
                'proxy': proxy
            },
            callback=self.parse_results
        )

    def parse_results(self, response):
        results = response.css('a.result__a::attr(href)').getall()
        for result in results:
            if self.results_fetched < self.limit:
                self.results.append({'url': result})
                self.results_fetched += 1
                yield {'url': result}
            else:
                break

        if self.results_fetched < self.limit:
            next_page = response.css('a.result--more__btn::attr(href)').get()
            if next_page:
                next_page_url = response.urljoin(next_page)
                
                if self.use_tor:
                    proxy = get_tor_proxy()
                    tor_manager.renew_tor_ip()
                else:
                    proxy = proxy_manager.get_random_proxy()

                yield scrapy.Request(
                    url=next_page_url,
                    meta={'playwright': True, 'proxy': proxy},
                    callback=self.parse_results
                )
        else:
            cache_manager.cache_results(self.query, 'duckduckgo', self.results)

    def closed(self, reason):
        with open('output.json', 'w') as f:
            json.dump(self.results, f, indent=4)