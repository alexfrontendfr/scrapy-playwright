import scrapy
from scrapy_playwright.page import PageCoroutine

class BingSpider(scrapy.Spider):
    name = "bing_spider"
    allowed_domains = ["bing.com"]
    start_urls = ["https://www.bing.com"]

    custom_settings = {
        "PLAYWRIGHT_LAUNCH_OPTIONS": {"headless": True},
        "RETRY_ENABLED": True,
        "RETRY_TIMES": 5,  # Retry failed requests up to 5 times
        "DOWNLOAD_TIMEOUT": 60  # Timeout after 60 seconds
    }

    def start_requests(self):
        search_query = getattr(self, 'query', 'web scraping with Scrapy')  # default query if not provided
        for url in self.start_urls:
            yield scrapy.Request(
                url, 
                meta=dict(
                    playwright=True,
                    playwright_page_coroutines=[
                        PageCoroutine("wait_for_selector", "input[name=q]"),
                        PageCoroutine("fill", "input[name=q]", search_query),
                        PageCoroutine("click", "input[type=submit]"),
                        PageCoroutine("wait_for_selector", "li.b_algo"),
                    ],
                )
            )

    def parse(self, response):
        if response.status != 200:
            self.logger.error(f"Failed to retrieve {response.url}")
            return
        
        for result in response.css("li.b_algo"):
            yield {
                "title": result.css("h2 a::text").get(),
                "link": result.css("h2 a::attr(href)").get(),
                "snippet": result.css(".b_caption p::text").get(),
            }
