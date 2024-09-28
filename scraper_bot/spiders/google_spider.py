import scrapy
from scraper_bot.spiders.base_spider import BaseSpider
from scrapy_playwright.page import PageMethod
from scraper_bot.utils.cache_manager import cache_manager
import json

class GoogleSpider(BaseSpider):
    name = "google_spider"
    
    def start_requests(self):
        cached_results = cache_manager.get_cached_results(self.query, 'google')
        if cached_results:
            self.logger.info(f"Using cached results for query: {self.query}")
            for result in cached_results[:self.limit]:
                yield self.process_result(result)
            return

        url = f"https://www.google.com/search?q={self.query}"
        proxy = self.get_proxy()

        yield scrapy.Request(
            url=url,
            meta={
                'playwright': True,
                'playwright_include_page': True,
                'playwright_page_methods': [
                    PageMethod('wait_for_selector', 'div.yuRUbf > a')
                ],
                'proxy': proxy
            },
            callback=self.parse_results
        )

    async def parse_results(self, response):
        page = response.meta['playwright_page']
        
        results = await page.query_selector_all('div.yuRUbf > a')
        for result in results:
            if self.results_fetched >= self.limit:
                break
            url = await result.get_attribute('href')
            yield self.process_result({'url': url})

        if self.results_fetched < self.limit:
            next_page = await page.query_selector('a#pnnext')
            if next_page:
                next_page_url = await next_page.get_attribute('href')
                proxy = self.get_proxy()

                yield scrapy.Request(
                    url=response.urljoin(next_page_url),
                    meta={
                        'playwright': True,
                        'playwright_include_page': True,
                        'playwright_page_methods': [
                            PageMethod('wait_for_selector', 'div.yuRUbf > a')
                        ],
                        'proxy': proxy
                    },
                    callback=self.parse_results
                )
        else:
            cache_manager.cache_results(self.query, 'google', self.results)

        await page.close()

    def closed(self, reason):
        super().closed(reason)
        with open('output.json', 'w') as f:
            json.dump(self.results, f, indent=4)