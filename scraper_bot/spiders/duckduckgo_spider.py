from scraper_bot.spiders.base_spider import BaseSpider
from bs4 import BeautifulSoup
from urllib.parse import quote_plus, urljoin

class DuckDuckGoSpider(BaseSpider):
    name = 'duckduckgo_spider'

    def get_search_url(self):
        return f'https://duckduckgo.com/html?q={quote_plus(self.query)}'

    async def parse_results(self, page):
        content = await page.content()
        soup = BeautifulSoup(content, 'lxml')
        results = []
        
        for result in soup.select('div.result'):
            title_elem = result.select_one('h2.result__title a')
            snippet_elem = result.select_one('a.result__snippet')
            
            if title_elem and snippet_elem:
                results.append({
                    'title': title_elem.text.strip(),
                    'url': title_elem['href'],
                    'snippet': snippet_elem.text.strip()
                })
        
        return results

    async def get_next_page(self, page):
        next_link = await page.query_selector('input[value="Next"]')
        if next_link:
            form = await page.query_selector('form#links_wrapper')
            if form:
                await form.evaluate('form => form.submit()')
                await page.wait_for_load_state('networkidle')
                return page.url
        return None