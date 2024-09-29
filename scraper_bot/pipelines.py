from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from scraper_bot.models import Base, ScraperResult
from scraper_bot import settings

class WebScraperPipeline:
    def __init__(self):
        self.engine = create_engine(settings.DATABASE_URL)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    def process_item(self, item, spider):
        session = self.Session()
        try:
            result = ScraperResult(
                query=spider.query,
                engine=spider.name,
                title=item['title'],
                url=item['url'],
                snippet=item['snippet']
            )
            session.add(result)
            session.commit()
        except Exception as e:
            spider.logger.error(f"Error saving result to database: {str(e)}")
            session.rollback()
        finally:
            session.close()
        return item