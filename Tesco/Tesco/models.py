from sqlalchemy import create_engine, Column
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Integer, String, Float, Text
from sqlalchemy.dialects.mysql import LONGTEXT
from scrapy.utils.project import get_project_settings

DeclarativeBase = declarative_base()

def db_connect():
    return create_engine(get_project_settings().get("CONNECTION_STRING"),  pool_pre_ping=True)

def create_table(engine):
    DeclarativeBase.metadata.create_all(engine)

class ProductRow(DeclarativeBase):
    __tablename__ = 'products'
    id = Column(Integer, autoincrement=True, primary_key=True)
    product_URL = Column(Text())
    product_ID = Column(Integer())
    image_URL = Column(Text())
    product_title = Column(String(100))
    category = Column(String(110))
    price = Column(Float())
    product_description = Column(Text())
    name_and_address = Column(Text())
    return_address = Column(Text())
    net_contents = Column(Text())
    review_title = Column(Text())
    stars_count = Column(Text())
    author = Column(Text())
    date = Column(Text())
    review_text = Column(LONGTEXT())
    usually_urls = Column(Text())
    usually_titles = Column(Text())
    usually_prices = Column(Text())
    usually_img_urls = Column(Text())