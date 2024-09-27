import scrapy
from scrapy_playwright.page import PageCoroutine

class OnionSpider(scrapy.Spider):
    name = "onion_spider"
    allowed_domains = [".onion"]
    
    # Adding more .onion sources for comprehensive dark web scraping
    start_urls = [
        "http://msydqstlz2kzerdg.onion",  # Ahmia search engine
        "http://hss3uro2hsxfogfq.onion",  # Torch search engine
        "http://xmh57jrzrnw6insl.onion",  # DuckDuckGo for .onion
        "http://grams7enufi7jmdl.onion",  # Grams search engine
        "http://torlinkbgs6aabns.onion",  # TorLinks directory
        "http://deepwebwikiidwd.onion"    # Deep Web Wiki
    ]

    custom_settings = {
        "PLAYWRIGHT_LAUNCH_OPTIONS": {
            "headless": True,
            "args": ["--proxy-server=socks5://127.0.0.1:9050"]
        }
    }

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(
                url,
                meta=dict(
                    playwright=True,
                    playwright_page_coroutines=[
                        PageCoroutine("wait_for_selector", "h1, h2"),
                    ],
                ),
                headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"},
            )

    def parse(self, response):
        # Enhanced error handling to capture failed requests or malformed pages
        if response.status != 200:
            self.logger.error(f"Failed to retrieve {response.url}")
            return

        for result in response.css("h1, h2"):
            yield {
                "heading": result.css("::text").get(),
                "link": response.url,
                "snippet": result.css("p::text").get(),
            }
