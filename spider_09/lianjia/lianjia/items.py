# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class LianjiaItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # id = scrapy.Field()
    title = scrapy.Field()
    position = scrapy.Field()
    huxing = scrapy.Field()
    mianji = scrapy.Field()
    chaoxiang = scrapy.Field()
    zhangxiu = scrapy.Field()
    louceng = scrapy.Field()
    nianfen = scrapy.Field()
    jiegou = scrapy.Field()
    pass
