# * coding: utf8 *

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Item, Field

class TescospiderItem(Item):
    product_URL = Field() 
    product_ID = Field() 
    image_URL = Field() 
    product_title = Field() 
    category = Field() 
    price = Field()
    product_description = Field() 
    name_and_address = Field() 
    return_address = Field() 
    net_contents = Field()
    review_title = Field()
    stars_count = Field()
    author = Field()
    date = Field()
    review_text = Field()
    usually_urls = Field()
    usually_titles = Field()
    usually_prices = Field()
    usually_img_urls = Field()