# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider
from ..items import TescospiderItem as productItem 
import logging
class ProductinfoSpider(CrawlSpider):
    name = 'ProductInfo'
    allowed_domains = ['www.tesco.com']
    start_urls = [
        'https://www.tesco.com/groceries/en-GB/shop/household/kitchen-roll-and-tissues/all',
        'https://www.tesco.com/groceries/en-GB/shop/pets/cat-food-and-accessories/all'
        

    ]

    def parse(self, response):
        for item in response.css('li.product-list--list-item'):
            link = item.css('a.product-image-wrapper').attrib['href']
            yield response.follow(link, self.product_info)
        next_page = response.xpath('//nav[contains(@class, "pagination--page-selector-wrapper")]/ul/li[last()]/a/@href').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
            
    def product_info(self, response):
        self.logger.info('Parse function called on %s', response.url)
        p_item = productItem()
        p_item['product_URL'] = response.url
        p_item['product_ID'] = int(response.url.split('/')[-1])
        p_item['image_URL'] = response.xpath('//img[contains(@class,"product-image")]/@srcset').get()
        p_item['product_title'] = response.xpath('//h1/text()').get()     
        p_item['category'] = response.xpath('//span[contains(@class," hWdmzc")]/text()').getall()[-1]
        p_item['name_and_address'] = \
            ''.join(response.xpath('//div[contains(@id, "manufacturer-address")]/ul/descendant::*/text()').getall())
        p_item['return_address'] = \
             ''.join(response.xpath('//div[contains(@id, "return-address")]/ul/descendant::*/text()').getall())
        p_item['net_contents'] = \
                response.xpath('//div[contains(@id, "net-contents")]/p/text()').get()
        part_descr_1 = \
            response.xpath('//div[contains(@id, "product-description")]/ul/descendant::*/text()').get(default='') 
        part_descr_2 = \
            response.xpath('//div[contains(@id, "product-marketing")]/ul/descendant::*/text()').get(default='')
        part_descr_3 = \
            response.xpath('//div[contains(@id, "pack-size")]/ul/descendant::*/text()').get(default='')
        p_item['product_description'] = ''.join([part_descr_1,part_descr_2,part_descr_3])
        p_item['price'] = float(response.xpath('//*[contains(@class, "value")]/text()').get(default=0))
        p_item['usually_urls'] = response.xpath('//div[contains(@class, "tile-content")]/a/@href').getall()
        p_item['usually_titles'] = response.xpath('//h3[contains(@class, "jEHaJJ")]/a/text()').getall()
        p_item['usually_prices'] = \
            [float(i) for i in response.xpath('//div[@class="price-control-wrapper"]//span[@class="value"]/text()').getall()[1:]]        
        p_item['usually_img_urls'] = \
            response.xpath('//div[@class="product-image__container"]/img/@src').getall()[1:]
        return self.get_reviews(response, item=p_item) 
    
    def get_reviews(self, response, **kw):
        p_item = kw.get("item")
        if p_item.get('review_title'):
            p_item['review_title'] = p_item.get('review_title') + \
                response.xpath('//h3[@class="review__summary"]/text()').getall() 
            p_item['stars_count'] = p_item.get('stars_count') + \
                [int(i.replace(' stars', '')) for i in response.xpath('//span[contains(@class, "czgxkL")]/text()').getall()[2:]]
            p_item['author']= p_item.get('author') + \
                response.xpath('//p[contains(@class, "review__syndication")]/text()').getall()
            p_item['date']= p_item.get('date') + \
                response.xpath('//span[contains(@class, "review-author__submission-time")]/text()').getall()
            p_item['review_text']= p_item.get('review_text') + \
                response.xpath('//p[contains(@class, "review__text")]/text()').getall()
        else:
            p_item['review_title'] = response.xpath('//h3[@class="review__summary"]/text()').getall()
            p_item['stars_count'] = [int(i.replace(' stars', '')) for i in response.xpath('//span[contains(@class, "czgxkL")]/text()').getall()[2:]]
            p_item['author'] = response.xpath('//p[contains(@class, "review__syndication")]/text()').getall()
            p_item['date'] = response.xpath('//span[contains(@class, "review-author__submission-time")]/text()').getall()
            p_item['review_text'] = response.xpath('//p[contains(@class, "review__text")]/text()').getall()

        
        next_reviews = response.xpath('//a[contains(@class, "GMOgz")]/@href').get()
        if next_reviews:
            yield response.follow(next_reviews, callback=self.get_reviews, cb_kwargs={'item':p_item})
        else:
            p_item['stars_count'] = sum(p_item.get('stars_count'))
            print(p_item.get('stars_count'),p_item.get('product_URL') )
            return p_item