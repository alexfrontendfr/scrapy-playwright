import random
import base64

class RandomUserAgentMiddleware:
    """Middleware to rotate user agents for each request."""
    def __init__(self, user_agents):
        self.user_agents = user_agents

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings.getlist('USER_AGENTS'))

    def process_request(self, request, spider):
        request.headers['User-Agent'] = random.choice(self.user_agents)


class ProxyMiddleware:
    """Middleware to rotate proxies for each request."""
    def __init__(self, proxies, proxy_auth=None):
        self.proxies = proxies
        self.proxy_auth = proxy_auth

    @classmethod
    def from_crawler(cls, crawler):
        # Load proxies and optional authentication from settings
        proxies = crawler.settings.getlist('PROXIES')
        proxy_auth = crawler.settings.get('PROXY_AUTH')
        return cls(proxies, proxy_auth)

    def process_request(self, request, spider):
        # Choose a random proxy from the list
        proxy = random.choice(self.proxies)
        request.meta['proxy'] = proxy

        # Add proxy authentication if needed
        if self.proxy_auth:
            user_pass = base64.b64encode(self.proxy_auth.encode()).decode('utf-8')
            request.headers['Proxy-Authorization'] = f'Basic {user_pass}'

    def process_exception(self, request, exception, spider):
        spider.logger.error(f"Proxy failed: {request.meta.get('proxy')}")

# Settings example for proxies and user agents:
# USER_AGENTS = [
#     "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
#     "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Safari/605.1.15",
#     "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36"
# ]
# PROXIES = [
#     'http://proxy1.example.com:8080',
#     'http://proxy2.example.com:8080',
#     'http://proxy3.example.com:8080'
# ]
# PROXY_AUTH = 'username:password'
