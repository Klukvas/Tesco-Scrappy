# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

from sqlalchemy.orm import sessionmaker
from Tesco.models import ProductRow, db_connect, create_table
import logging


class TescoPipeline:
    def __init__(self):
        engine = db_connect()
        create_table(engine)
        self.Session = sessionmaker(bind=engine)
    def process_item(self, item, spider):
        session = self.Session()
        new_product = ProductRow()
        new_product.product_URL = str(item['product_URL'])
        new_product.product_ID = item['product_ID']
        new_product.image_URL = item['image_URL'] 
        new_product.product_title = item['product_title'] 
        new_product.category = item['category'] 
        new_product.price = item['price'] 
        new_product.product_description = item['product_description'] 
        new_product.name_and_address = item['name_and_address'] 
        new_product.return_address = item['return_address'] 
        new_product.net_contents =  item['net_contents']
        new_product.review_title =  item['review_title']
        new_product.stars_count = item['stars_count']
        new_product.author = item['author'] 
        new_product.date = item['date'] 
        new_product.review_text = item['review_text'] 
        new_product.usually_urls =  item['usually_urls']
        new_product.usually_titles = item['usually_titles'] 
        new_product.usually_prices = item['usually_prices'] 
        new_product.usually_img_urls = item['usually_img_urls'] 
        
        try:
            logging.info(f'Product #{item["product_ID"]} successfully added to DB')
            session.merge(new_product)
            session.commit()
        except:
            logging.critical(f'Product #{item["product_ID"]} failed added  to DB')
            session.rollback()
            raise
        finally:
            session.close()

        return item

    def open_spider(self, spider):
        logging.info('Spider {} start'.format(spider))
    
    def close_spider(self, spider):
        logging.info('Spider {} end'.format(spider))