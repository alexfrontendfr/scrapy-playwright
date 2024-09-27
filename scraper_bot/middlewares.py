# File: scraper_bot/middlewares.py
import random
from scrapy.utils.project import get_project_settings

# Middleware for rotating user agents
class RandomUserAgentMiddleware:
    def __init__(self, user_agents):
        self.user_agents = user_agents

    @classmethod
    def from_crawler(cls, crawler):
        # Corrected to use 'USER_AGENT_LIST' from settings
        return cls(user_agents=crawler.settings.get('USER_AGENT_LIST'))

    def process_request(self, request, spider):
        user_agent = random.choice(self.user_agents)
        request.headers['User-Agent'] = user_agent
        spider.logger.info(f'Using User-Agent: {user_agent}')


# Middleware for rotating proxies
class ProxyMiddleware:
    def __init__(self):
        self.settings = get_project_settings()
        self.proxies = self.settings.get('PROXY_LIST', [])  # Fetch the full proxy list

    def process_request(self, request, spider):
        if self.proxies:
            proxy = random.choice(self.proxies)
            request.meta['proxy'] = proxy
            spider.logger.info(f'Using proxy: {proxy}')
        else:
            spider.logger.warning('No proxies available in PROXY_LIST.')

    def process_exception(self, request, exception, spider):
        # If a request fails due to a proxy issue, retry with another proxy
        if self.proxies:
            new_proxy = random.choice(self.proxies)
            request.meta['proxy'] = new_proxy
            spider.logger.info(f'Retrying with a new proxy: {new_proxy}')
            return request
