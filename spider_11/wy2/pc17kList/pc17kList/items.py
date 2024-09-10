# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Pc17KlistItem(scrapy.Item):
    # define the fields for your item here like:
    id = scrapy.Field()
    type = scrapy.Field()
    book_name = scrapy.Field()
    latest_chapter = scrapy.Field()
    word_count = scrapy.Field()
    author = scrapy.Field()
    update_time = scrapy.Field()
    state = scrapy.Field()
    detail_url = scrapy.Field()
    pass
