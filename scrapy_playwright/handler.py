import asyncio
from playwright.async_api import async_playwright

class PlaywrightHandler:
    """
    Handles all interactions with the Playwright browser, including launching,
    managing browser contexts, and scraping pages.
    """
    def __init__(self):
        self.browser = None
        self.context = None
        self.page = None

    async def launch_browser(self):
        """
        Launches a Chromium browser instance using Playwright in headless mode.
        """
        playwright = await async_playwright().start()
        self.browser = await playwright.chromium.launch(headless=True)
        self.context = await self.browser.new_context()
        self.page = await self.context.new_page()

    async def scrape(self, url):
        """
        Visits the provided URL and returns the page content. Custom scraping logic
        can be added here for specific elements, titles, etc.
        """
        await self.page.goto(url)
        content = await self.page.content()
        await self.close_browser()
        return content

    async def close_browser(self):
        """
        Closes the browser and cleans up the browser context.
        """
        await self.page.close()
        await self.context.close()
        await self.browser.close()

# Example usage of the PlaywrightHandler class
async def scrape_url(url):
    handler = PlaywrightHandler()
    await handler.launch_browser()
    result = await handler.scrape(url)
    return result
