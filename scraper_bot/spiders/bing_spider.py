import scrapy
from scrapy_playwright.page import PageCoroutine
import json
from scraper_bot.utils.proxy_helper import proxy_manager, tor_manager, get_tor_proxy
from scraper_bot.utils.cache_manager import cache_manager

class BingSpider(scrapy.Spider):
    name = "bing_spider"
    
    def __init__(self, query=None, limit=50, use_tor=False, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.query = query
        self.limit = int(limit)
        self.results_fetched = 0
        self.use_tor = use_tor == 'true'
        self.results = []

    def start_requests(self):
        cached_results = cache_manager.get_cached_results(self.query, 'bing')
        if cached_results:
            self.logger.info(f"Using cached results for query: {self.query}")
            for result in cached_results:
                yield result
            return

        url = f"https://www.bing.com/search?q={self.query}"
        
        if self.use_tor:
            proxy = get_tor_proxy()
            tor_manager.renew_tor_ip()
        else:
            proxy = proxy_manager.get_random_proxy()

        yield scrapy.Request(
            url=url,
            meta={
                'playwright': True,
                'playwright_include_page': True,
                'proxy': proxy
            },
            callback=self.parse_results
        )

    async def parse_results(self, response):
        page = response.meta['playwright_page']
        await page.wait_for_selector('li.b_algo h2 a')
        
        results = await page.query_selector_all('li.b_algo h2 a')
        for result in results:
            if self.results_fetched < self.limit:
                url = await result.get_attribute('href')
                self.results.append({'url': url})
                self.results_fetched += 1
                yield {'url': url}
            else:
                break

        if self.results_fetched < self.limit:
            next_page = await page.query_selector('a.sb_pagN')
            if next_page:
                next_page_url = await next_page.get_attribute('href')
                
                if self.use_tor:
                    proxy = get_tor_proxy()
                    tor_manager.renew_tor_ip()
                else:
                    proxy = proxy_manager.get_random_proxy()

                yield scrapy.Request(
                    url=response.urljoin(next_page_url),
                    meta={'playwright': True, 'playwright_include_page': True, 'proxy': proxy},
                    callback=self.parse_results
                )
        else:
            cache_manager.cache_results(self.query, 'bing', self.results)

        await page.close()

    def closed(self, reason):
        with open('output.json', 'w') as f:
            json.dump(self.results, f, indent=4)