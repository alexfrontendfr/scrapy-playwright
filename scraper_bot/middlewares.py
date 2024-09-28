# File: scraper_bot/middlewares.py
import random
from scrapy.utils.project import get_project_settings
from scraper_bot.utils.proxy_helper import proxy_manager, tor_manager, get_tor_proxy

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
        if spider.use_tor:
            request.meta['proxy'] = get_tor_proxy()
            tor_manager.renew_tor_ip()
        else:
            request.meta['proxy'] = proxy_manager.get_random_proxy()

    def process_exception(self, request, exception, spider):
        if not spider.use_tor:
            new_proxy = proxy_manager.get_random_proxy()
            request.meta['proxy'] = new_proxy
            return request