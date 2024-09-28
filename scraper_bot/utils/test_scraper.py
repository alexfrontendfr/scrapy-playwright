import unittest
from unittest.mock import patch, MagicMock
from scrapy.http import HtmlResponse
from scraper_bot.spiders.base_spider import BaseSpider
from scraper_bot.spiders.google_spider import GoogleSpider
from scraper_bot.spiders.bing_spider import BingSpider
from scraper_bot.spiders.duckduckgo_spider import DuckDuckGoSpider
from scraper_bot.spiders.onion_spider import OnionSpider
from scraper_bot.spiders.keyword_spider import KeywordSpider
from scraper_bot.utils.cache_manager import CacheManager
from scraper_bot.utils.proxy_helper import ProxyManager, TorManager

class MockSpider(BaseSpider):
    name = "mock_spider"

    def parse(self, response):
        for item in response.css('div.result'):
            yield self.process_result({
                'title': item.css('h2::text').get(),
                'url': item.css('a::attr(href)').get(),
            })

class TestScraperBot(unittest.TestCase):

    def setUp(self):
        self.cache_manager = CacheManager(cache_dir='test_cache')
        self.proxy_manager = ProxyManager()
        self.tor_manager = TorManager()

    def test_base_spider(self):
        spider = MockSpider(query="test", limit=5)
        html = '''
        <html>
            <body>
                <div class="result"><h2>Result 1</h2><a href="http://example1.com">Link 1</a></div>
                <div class="result"><h2>Result 2</h2><a href="http://example2.com">Link 2</a></div>
            </body>
        </html>
        '''
        response = HtmlResponse(url="http://example.com", body=html, encoding='utf-8')
        results = list(spider.parse(response))
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0]['title'], 'Result 1')
        self.assertEqual(results[0]['url'], 'http://example1.com')

    def test_google_spider(self):
        spider = GoogleSpider(query="test", limit=5, use_tor=False)
        self.assertEqual(spider.name, 'google_spider')
        self.assertEqual(spider.query, 'test')
        self.assertEqual(spider.limit, 5)
        self.assertFalse(spider.use_tor)

    def test_bing_spider(self):
        spider = BingSpider(query="test", limit=5, use_tor=False)
        self.assertEqual(spider.name, 'bing_spider')
        self.assertEqual(spider.query, 'test')
        self.assertEqual(spider.limit, 5)
        self.assertFalse(spider.use_tor)

    def test_duckduckgo_spider(self):
        spider = DuckDuckGoSpider(query="test", limit=5, use_tor=False)
        self.assertEqual(spider.name, 'duckduckgo_spider')
        self.assertEqual(spider.query, 'test')
        self.assertEqual(spider.limit, 5)
        self.assertFalse(spider.use_tor)

    def test_onion_spider(self):
        spider = OnionSpider(query="test", limit=5, use_tor=True)
        self.assertEqual(spider.name, 'onion_spider')
        self.assertEqual(spider.query, 'test')
        self.assertEqual(spider.limit, 5)
        self.assertTrue(spider.use_tor)

    def test_keyword_spider(self):
        spider = KeywordSpider(query="test", limit=5)
        self.assertEqual(spider.name, 'keyword_spider')
        self.assertEqual(spider.query, 'test')
        self.assertEqual(spider.limit, 5)

    def test_cache_manager(self):
        results = [{'url': 'https://example.com', 'title': 'Example'}]
        self.cache_manager.cache_results('test_query', 'google', results)
        cached_results = self.cache_manager.get_cached_results('test_query', 'google')
        self.assertEqual(cached_results, results)

    @patch('requests.get')
    def test_proxy_manager(self, mock_get):
        mock_response = MagicMock()
        mock_response.text = '1.1.1.1:8080\n2.2.2.2:8080'
        mock_get.return_value = mock_response

        proxies = self.proxy_manager.get_proxies()
        self.assertEqual(len(proxies), 2)
        self.assertIn('1.1.1.1:8080', proxies)
        self.assertIn('2.2.2.2:8080', proxies)

    @patch('stem.control.Controller.from_port')
    def test_tor_manager(self, mock_controller):
        mock_controller.return_value.__enter__.return_value.signal.return_value = None
        self.tor_manager.renew_tor_ip()
        mock_controller.return_value.__enter__.return_value.signal.assert_called_once()

    def test_spider_proxy_usage(self):
        spider = MockSpider(query="test", limit=5, use_tor=False)
        proxy = spider.get_proxy()
        self.assertIsNotNone(proxy)

        spider.use_tor = True
        tor_proxy = spider.get_proxy()
        self.assertEqual(tor_proxy, 'socks5://127.0.0.1:9050')

if __name__ == '__main__':
    unittest.main()