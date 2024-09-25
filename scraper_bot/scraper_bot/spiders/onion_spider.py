import scrapy

class OnionSpider(scrapy.Spider):
    name = 'onion_spider'
    start_urls = ['http://duskgytldkxiuqc6.onion', 'http://3g2upl4pq6kufc4m.onion']


    def parse(self, response):
        page_title = response.css('title::text').get()
        yield {
            'url': response.url,
            'title': page_title,
        }
