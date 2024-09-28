import scrapy
from scraper_bot.spiders.base_spider import BaseSpider
from scrapy_playwright.page import PageMethod
from scraper_bot.utils.cache_manager import cache_manager
import json

class DuckDuckGoSpider(BaseSpider):
    name = "duckduckgo_spider"
    
    def start_requests(self):
        cached_results = cache_manager.get_cached_results(self.query, 'duckduckgo')
        if cached_results:
            self.logger.info(f"Using cached results for query: {self.query}")
            for result in cached_results:
                yield self.process_result(result)
            return

        url = f"https://duckduckgo.com/?q={self.query}"
        proxy = self.get_proxy()

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
            yield self.process_result({'url': result})

        if self.results_fetched < self.limit:
            next_page = response.css('a.result--more__btn::attr(href)').get()
            if next_page:
                next_page_url = response.urljoin(next_page)
                proxy = self.get_proxy()

                yield scrapy.Request(
                    url=next_page_url,
                    meta={'playwright': True, 'proxy': proxy},
                    callback=self.parse_results
                )
        else:
            cache_manager.cache_results(self.query, 'duckduckgo', self.results)

    def closed(self, reason):
        super().closed(reason)
        with open('output.json', 'w') as f:
            json.dump(self.results, f, indent=4)