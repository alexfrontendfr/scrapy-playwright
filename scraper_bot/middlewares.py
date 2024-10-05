import random
from scrapy.exceptions import NotConfigured
from scraper_bot.utils.proxy_config import proxy_manager

class RandomUserAgentMiddleware:
    def __init__(self, user_agents):
        self.user_agents = user_agents

    @classmethod
    def from_crawler(cls, crawler):
        user_agents = crawler.settings.get('USER_AGENT_LIST', [])
        if not user_agents:
            raise NotConfigured("USER_AGENT_LIST setting is empty or not set")
        return cls(user_agents)

    def process_request(self, request, spider):
        request.headers['User-Agent'] = random.choice(self.user_agents)

class ProxyMiddleware:
    def process_request(self, request, spider):
        if not getattr(spider, 'use_tor', False):
            proxy = proxy_manager.get_random_proxy()
            if proxy:
                request.meta['proxy'] = proxy

    def process_exception(self, request, exception, spider):
        if not getattr(spider, 'use_tor', False):
            proxy = proxy_manager.get_random_proxy()
            if proxy:
                request.meta['proxy'] = proxy
            return request