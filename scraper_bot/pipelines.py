from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
from scraper_bot.utils.error_handler import error_handler

class DuplicateFilter:
    def __init__(self):
        self.urls_seen = set()

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        if adapter['url'] in self.urls_seen:
            raise DropItem(f"Duplicate item found: {item!r}")
        self.urls_seen.add(adapter['url'])
        return item

class ContentCleaner:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        adapter['title'] = adapter.get('title', '').strip()
        adapter['snippet'] = adapter.get('snippet', '').strip()
        return item

class DataValidator:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        if not adapter.get('url'):
            error_handler.handle_item_error(item, spider.crawler.stats)
            raise DropItem("Missing URL in item")
        return item

class ScraperBotPipeline:
    def __init__(self):
        self.duplicate_filter = DuplicateFilter()
        self.content_cleaner = ContentCleaner()
        self.data_validator = DataValidator()

    def process_item(self, item, spider):
        item = self.duplicate_filter.process_item(item, spider)
        item = self.content_cleaner.process_item(item, spider)
        item = self.data_validator.process_item(item, spider)
        return item