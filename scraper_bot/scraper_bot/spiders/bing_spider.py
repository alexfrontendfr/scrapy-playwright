
import scrapy
from bs4 import BeautifulSoup

class BingSpider(scrapy.Spider):
    name = 'bing_spider'
    
    def __init__(self, keyword=None, *args, **kwargs):
        super(BingSpider, self).__init__(*args, **kwargs)
        if keyword:
            self.search_query = keyword
        else:
            self.search_query = "default search"
    
    def start_requests(self):
        query = self.search_query.replace(' ', '+')
        search_url = f'https://www.bing.com/search?q={query}'
        yield scrapy.Request(url=search_url, callback=self.parse_results)
    
    def parse_results(self, response):
        soup = BeautifulSoup(response.body, 'html.parser')
        
        # Scraping URLs from Bing search results
        for link in soup.find_all('a'):
            website_url = link.get('href')
            yield {'website': website_url}
