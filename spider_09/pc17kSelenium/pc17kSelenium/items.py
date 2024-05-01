# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Pc17KseleniumItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    type = scrapy.Field()
    name = scrapy.Field()
    updatetime = scrapy.Field()
    author = scrapy.Field()
    pass
