import scrapy
from scrapy_playwright.page import PageCoroutine

class KeywordSpider(scrapy.Spider):
    name = "keyword_spider"
    allowed_domains = ["duckduckgo.com"]
    start_urls = ["https://duckduckgo.com"]

    custom_settings = {
        "PLAYWRIGHT_LAUNCH_OPTIONS": {"headless": True},
        "RETRY_ENABLED": True,
        "RETRY_TIMES": 5,  # Retry failed requests up to 5 times
        "DOWNLOAD_TIMEOUT": 60  # Timeout after 60 seconds
    }

    def start_requests(self):
        keyword = getattr(self, "keyword", "scrapy python")  # default keyword if not provided
        for url in self.start_urls:
            yield scrapy.Request(
                url, 
                meta=dict(
                    playwright=True,
                    playwright_page_coroutines=[
                        PageCoroutine("wait_for_selector", "input[name=q]"),
                        PageCoroutine("fill", "input[name=q]", keyword),
                        PageCoroutine("click", "input[type=submit]"),
                        PageCoroutine("wait_for_selector", "div.result__body"),
                    ],
                )
            )

    def parse(self, response):
        if response.status != 200:
            self.logger.error(f"Failed to retrieve {response.url}")
            return
        
        for result in response.css("div.result__body"):
            yield {
                "title": result.css("h2 a::text").get(),
                "link": result.css("h2 a::attr(href)").get(),
                "snippet": result.css(".result__snippet::text").get(),
            }
