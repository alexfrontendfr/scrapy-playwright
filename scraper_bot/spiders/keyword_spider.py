import scrapy
from scraper_bot.spiders.base_spider import BaseSpider
from scrapy_playwright.page import PageMethod
import random
from scraper_bot.utils.proxy_helper import get_proxies, get_tor_proxy
from scraper_bot.utils.cache_manager import cache_manager
import json
from urllib.parse import urlencode, urljoin

class KeywordSpider(BaseSpider):
    name = "keyword_spider"

    def __init__(self, query=None, limit=50, use_tor=False, *args, **kwargs):
        super().__init__(query, limit, use_tor, *args, **kwargs)
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36'
        ]
        self.proxies = get_proxies() if not use_tor else [get_tor_proxy()]

    def start_requests(self):
        cached_results = cache_manager.get_cached_results(self.query, 'keyword')
        if cached_results:
            self.logger.info(f"Using cached results for query: {self.query}")
            for result in cached_results[:self.limit]:
                yield self.process_result(result)
            return

        search_engines = [
            ("https://www.google.com/search", {'q': self.query}),
            ("https://www.bing.com/search", {'q': self.query}),
            ("https://duckduckgo.com/", {'q': self.query}),
        ]

        for base_url, params in search_engines:
            url = f"{base_url}?{urlencode(params)}"
            user_agent = random.choice(self.user_agents)
            proxy = random.choice(self.proxies)

            yield scrapy.Request(
                url=url,
                headers={'User-Agent': user_agent},
                meta={
                    'playwright': True,
                    'playwright_include_page': True,
                    'playwright_page_methods': [
                        PageMethod('wait_for_selector', 'body'),
                    ],
                    'proxy': proxy,
                    'engine': base_url
                },
                callback=self.parse_results,
                errback=self.errback_httpbin,
            )

    async def parse_results(self, response):
        page = response.meta['playwright_page']
        engine = response.meta['engine']

        if 'google.com' in engine:
            results = await page.query_selector_all('.g')
            for result in results[:self.limit]:
                title_elem = await result.query_selector('.r > a > h3')
                link_elem = await result.query_selector('.r > a')
                snippet_elem = await result.query_selector('.s > .st')

                if title_elem and link_elem and snippet_elem:
                    title = await title_elem.inner_text()
                    link = await link_elem.get_attribute('href')
                    snippet = await snippet_elem.inner_text()
                    yield self.process_result({'title': title, 'url': link, 'snippet': snippet})

        elif 'bing.com' in engine:
            results = await page.query_selector_all('.b_algo')
            for result in results[:self.limit]:
                title_elem = await result.query_selector('h2 > a')
                snippet_elem = await result.query_selector('.b_caption > p')

                if title_elem and snippet_elem:
                    title = await title_elem.inner_text()
                    link = await title_elem.get_attribute('href')
                    snippet = await snippet_elem.inner_text()
                    yield self.process_result({'title': title, 'url': link, 'snippet': snippet})

        elif 'duckduckgo.com' in engine:
            results = await page.query_selector_all('.result')
            for result in results[:self.limit]:
                title_elem = await result.query_selector('.result__title > a')
                snippet_elem = await result.query_selector('.result__snippet')

                if title_elem and snippet_elem:
                    title = await title_elem.inner_text()
                    link = await title_elem.get_attribute('href')
                    snippet = await snippet_elem.inner_text()
                    yield self.process_result({'title': title, 'url': link, 'snippet': snippet})

        if self.results_fetched < self.limit:
            next_page = await page.query_selector('a.next') or await page.query_selector('a.pager__button--next')
            if next_page:
                next_page_url = await next_page.get_attribute('href')
                if next_page_url:
                    yield scrapy.Request(
                        url=urljoin(response.url, next_page_url),
                        meta=response.meta,
                        callback=self.parse_results,
                        errback=self.errback_httpbin,
                    )
        else:
            cache_manager.cache_results(self.query, 'keyword', self.results)

        await page.close()

    def errback_httpbin(self, failure):
        self.logger.error(f"Error occurred: {failure}")

    def closed(self, reason):
        super().closed(reason)
        with open('keyword_output.json', 'w') as f:
            json.dump(self.results, f, indent=4)