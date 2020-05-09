from sqlalchemy import create_engine, Column
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Integer, String, Float, Text

from scrapy.utils.project import get_project_settings

DeclarativeBase = declarative_base()

def db_connect():
    return create_engine(get_project_settings().get("CONNECTION_STRING"),  pool_pre_ping=True)

def create_table(engine):
    DeclarativeBase.metadata.create_all(engine)

class AbiturientRow(DeclarativeBase):
    __tablename__ = 'products'
    id = Column(Integer, autoincrement=True, primary_key=True)
    product_URL = Column(String(100))
    product_ID = Column(Integer())
    image_URL = Column(String(200))
    product_title = Column(String(100))
    category = Column(String(100))
    price = Column(Float())
    product_description = Column(Text())
    name_and_address = Column(String(100))
    return_address = Column(String(100))
    net_contents = Column(String(100))
    review_title = Column(Text())
    stars_count = Column(Text())
    author = Column(Text())
    date = Column(Text())
    review_text = Column(Text())
    usually_urls = Column(String(200))
    usually_titles = Column(String(200))
    usually_prices = Column(String(200))
    usually_img_urls = Column(String(300))