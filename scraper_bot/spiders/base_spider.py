import asyncio
from playwright.async_api import async_playwright
from scrapy import Spider
from scrapy.http import Request
from scrapy.utils.defer import maybe_deferred_to_future
from urllib.parse import urljoin

class BaseSpider(Spider):
    name = 'base_spider'

    def __init__(self, query=None, limit=10, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.query = query
        self.limit = int(limit)
        self.results = []

    async def start_requests(self):
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            
            url = self.get_search_url()
            await page.goto(url)
            
            while len(self.results) < self.limit:
                results = await self.parse_results(page)
                self.results.extend(results[:self.limit - len(self.results)])
                
                if len(self.results) < self.limit:
                    next_page = await self.get_next_page(page)
                    if not next_page:
                        break
                    await page.goto(next_page)
            
            await browser.close()
        
        for result in self.results:
            yield Request(url=result['url'], callback=self.parse_item, cb_kwargs={'item': result})

    async def parse_results(self, page):
        raise NotImplementedError

    async def get_next_page(self, page):
        raise NotImplementedError

    def get_search_url(self):
        raise NotImplementedError

    async def parse_item(self, response, item):
        yield item

    def parse(self, response):
        return maybe_deferred_to_future(self._parse(response))

    async def _parse(self, response):
        async for item in self.parse_item(response):
            yield item