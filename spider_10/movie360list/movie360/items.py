# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Movie360Item(scrapy.Item):
    movie_name = scrapy.Field()
    title_description = scrapy.Field()
    url = scrapy.Field()
    pass
