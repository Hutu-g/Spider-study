# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Pc17KdetailItem(scrapy.Item):
    # define the fields for your item here like:
    id = scrapy.Field()
    intro = scrapy.Field()
    auth_level = scrapy.Field()
    week_click = scrapy.Field()
    month_click = scrapy.Field()
    week_up = scrapy.Field()
    month_up = scrapy.Field()
    week_tick = scrapy.Field()
    month_tick = scrapy.Field()
    pass
