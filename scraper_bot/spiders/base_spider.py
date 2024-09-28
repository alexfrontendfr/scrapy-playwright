import scrapy
from scrapy.exceptions import CloseSpider
from scraper_bot.utils.proxy_helper import proxy_manager, tor_manager, get_tor_proxy

class BaseSpider(scrapy.Spider):
    def __init__(self, query=None, limit=50, use_tor=False, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.query = query
        self.limit = int(limit)
        self.results_fetched = 0
        self.use_tor = use_tor
        self.results = []

    def get_proxy(self):
        if self.use_tor:
            tor_manager.renew_tor_ip()
            return get_tor_proxy()
        return proxy_manager.get_random_proxy()

    def parse(self, response):
        raise NotImplementedError

    def process_result(self, result):
        if self.results_fetched < self.limit:
            self.results.append(result)
            self.results_fetched += 1
            yield result
            if self.results_fetched >= self.limit:
                raise CloseSpider(f'Reached result limit of {self.limit}')
        else:
            raise CloseSpider(f'Reached result limit of {self.limit}')

    def closed(self, reason):
        self.crawler.stats.set_value('results_fetched', self.results_fetched)