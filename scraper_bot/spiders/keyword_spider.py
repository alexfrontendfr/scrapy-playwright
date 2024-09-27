import scrapy
from scrapy_playwright.page import PageCoroutine
import random
from scraper_bot.utils.proxy_helper import get_proxies  # Import the helper function

class KeywordSpider(scrapy.Spider):
    name = "keyword_spider"
    
    def __init__(self, query=None, limit=50, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.query = query
        self.limit = int(limit)
        self.results_fetched = 0  # Track the number of results fetched
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) Chrome/90.0',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0'
        ]
        self.proxies = get_proxies()  # Fetch proxies dynamically at runtime

    def start_requests(self):
        url = f"https://genericsearchengine.com/?q={self.query}"
        user_agent = random.choice(self.user_agents)
        proxy = random.choice(self.proxies)  # Rotate proxies dynamically

        yield scrapy.Request(
            url=url,
            headers={'User-Agent': user_agent},
            meta={
                'playwright': True,
                'playwright_page_coroutines': [
                    PageCoroutine('wait_for_selector', '.result-title a')
                ],
                'proxy': proxy
            },
            callback=self.parse_results
        )

    def parse_results(self, response):
        # Handle the parsing logic for search results
        results = response.css('.result')
        for idx, result in enumerate(results):
            if self.results_fetched < self.limit:
                title = result.css('.result-title a::text').get()
                link = result.css('.result-title a::attr(href)').get()
                yield {'title': title, 'url': link}
                self.results_fetched += 1
            else:
                break

        # Follow pagination if results limit is not yet met
        if self.results_fetched < self.limit:
            next_page = response.css('a.pagination-next::attr(href)').get()
            if next_page:
                next_page_url = response.urljoin(next_page)
                user_agent = random.choice(self.user_agents)
                proxy = random.choice(self.proxies)

                yield scrapy.Request(
                    url=next_page_url,
                    headers={'User-Agent': user_agent},
                    meta={'playwright': True, 'proxy': proxy},
                    callback=self.parse_results
                )
