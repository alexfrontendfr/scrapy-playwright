from celery import Celery
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scraper_bot.spiders.google_spider import GoogleSpider
from scraper_bot.spiders.bing_spider import BingSpider
from scraper_bot.spiders.duckduckgo_spider import DuckDuckGoSpider
from scraper_bot.spiders.onion_spider import OnionSpider
from scraper_bot.utils.cache_manager import cache_manager

app = Celery('scraper_bot', broker=settings.REDIS_URL, backend=settings.REDIS_URL)

@app.task(bind=True)
def run_spider(self, spider_name, query, limit, use_tor):
    spider_class = {
        'google': GoogleSpider,
        'bing': BingSpider,
        'duckduckgo': DuckDuckGoSpider,
        'onion': OnionSpider,
    }.get(spider_name)

    if not spider_class:
        raise ValueError(f"Invalid spider name: {spider_name}")

    cached_results = cache_manager.get_cached_results(query, spider_name)
    if cached_results:
        return cached_results[:limit]

    settings = get_project_settings()
    process = CrawlerProcess(settings)
    process.crawl(spider_class, query=query, limit=limit, use_tor=use_tor)
    process.start()

    results = cache_manager.get_cached_results(query, spider_name)[:limit]

    for i, _ in enumerate(results):
        self.update_state(state='PROGRESS', meta={'current': i+1, 'total': len(results), 'status': f'Processing result {i+1} of {len(results)}'})

    return results