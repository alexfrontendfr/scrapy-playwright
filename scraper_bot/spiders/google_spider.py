from scraper_bot.spiders.base_spider import BaseSpider
from bs4 import BeautifulSoup
from urllib.parse import quote_plus, urljoin

class GoogleSpider(BaseSpider):
    name = 'google_spider'

    def get_search_url(self):
        return f'https://www.google.com/search?q={quote_plus(self.query)}'

    async def parse_results(self, page):
        content = await page.content()
        soup = BeautifulSoup(content, 'lxml')
        results = []
        
        for div in soup.select('div.g'):
            title_elem = div.select_one('h3.r')
            link_elem = div.select_one('div.r > a')
            snippet_elem = div.select_one('div.s')
            
            if title_elem and link_elem and snippet_elem:
                results.append({
                    'title': title_elem.text.strip(),
                    'url': link_elem['href'],
                    'snippet': snippet_elem.text.strip()
                })
        
        return results

    async def get_next_page(self, page):
        next_link = await page.query_selector('a#pnnext')
        if next_link:
            return await next_link.get_attribute('href')
        return None