from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class ScraperResult(Base):
    __tablename__ = 'scraper_results'

    id = Column(Integer, primary_key=True)
    query = Column(String(255))
    engine = Column(String(50))
    title = Column(String(255))
    url = Column(String(1000))
    snippet = Column(Text)
    scraped_at = Column(DateTime, default=datetime.utcnow)