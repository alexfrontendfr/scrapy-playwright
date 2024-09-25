import scrapy
from bs4 import BeautifulSoup

class KeywordSpider(scrapy.Spider):
    name = 'keyword_spider'
    
    def __init__(self, keyword=None, *args, **kwargs):
        super(KeywordSpider, self).__init__(*args, **kwargs)
        if keyword:
            self.search_query = keyword
        else:
            self.search_query = "gay community"

    def start_requests(self):
        query = self.search_query.replace(' ', '+')
        search_url = f'https://duckduckgo.com/html?q={query}'
        yield scrapy.Request(url=search_url, callback=self.parse_results)

    def parse_results(self, response):
        soup = BeautifulSoup(response.body, 'html.parser')
        
        # Scraping URLs from DuckDuckGo search results
        for link in soup.find_all('a', {'class': 'result__a'}):
            website_url = link.get('href')
            yield {'website': website_url}

    def close(self, reason):
        # Save the results in a unique JSON file for each search query
        output_file = f'{self.search_query.replace("+", "_")}_results.json'
        with open(output_file, 'w') as f:
            f.write(self.result_items)
