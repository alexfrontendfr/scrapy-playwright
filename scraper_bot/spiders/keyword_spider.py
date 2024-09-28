import scrapy
from scraper_bot.spiders.base_spider import BaseSpider
from scrapy_playwright.page import PageMethod
import random
from scraper_bot.utils.proxy_helper import get_proxies

class KeywordSpider(BaseSpider):
    name = "keyword_spider"

    def __init__(self, query=None, limit=50, use_tor=False, *args, **kwargs):
        super().__init__(query, limit, use_tor, *args, **kwargs)
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) Chrome/90.0',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0'
        ]
        self.proxies = get_proxies()

    def start_requests(self):
        url = f"https://genericsearchengine.com/?q={self.query}"
        user_agent = random.choice(self.user_agents)
        proxy = self.get_proxy()

        yield scrapy.Request(
            url=url,
            headers={'User-Agent': user_agent},
            meta={
                'playwright': True,
                'playwright_page_coroutines': [
                    PageMethod('wait_for_selector', '.result-title a')
                ],
                'proxy': proxy
            },
            callback=self.parse_results
        )

    def parse_results(self, response):
        results = response.css('.result')
        for result in results:
            title = result.css('.result-title a::text').get()
            link = result.css('.result-title a::attr(href)').get()
            yield self.process_result({'title': title, 'url': link})

        if self.results_fetched < self.limit:
            next_page = response.css('a.pagination-next::attr(href)').get()
            if next_page:
                next_page_url = response.urljoin(next_page)
                user_agent = random.choice(self.user_agents)
                proxy = self.get_proxy()

                yield scrapy.Request(
                    url=next_page_url,
                    headers={'User-Agent': user_agent},
                    meta={'playwright': True, 'proxy': proxy},
                    callback=self.parse_results
                )