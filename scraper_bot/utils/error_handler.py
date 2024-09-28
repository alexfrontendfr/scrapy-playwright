import logging
from scrapy.exceptions import IgnoreRequest

logger = logging.getLogger(__name__)

class ErrorHandler:
    @staticmethod
    def handle_spider_error(failure, response, spider):
        if failure.check(IgnoreRequest):
            return
        logger.error(f"Spider error on {response.url}: {str(failure)}")
        spider.crawler.stats.inc_value(f'error_count/{failure.type.__name__}')

    @staticmethod
    def handle_download_error(failure, request, spider):
        logger.error(f"Download error on {request.url}: {str(failure)}")
        spider.crawler.stats.inc_value(f'error_count/{failure.type.__name__}')

    @staticmethod
    def handle_item_error(item, spider):
        logger.error(f"Item processing error: {item}")
        spider.crawler.stats.inc_value('error_count/ItemError')

error_handler = ErrorHandler()