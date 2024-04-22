import scrapy
from scrapy import Selector,Request
from scrapy.http import HtmlResponse

from ..items import MovieItem


class Movietop250Spider(scrapy.Spider):
    name = "movieTop250"
    allowed_domains = ["movie.douban.com"]
    # start_urls = ["https://movie.douban.com/top250"]
    #
    def start_requests(self):
        for page in range(1):
            yield Request(url=f"https://movie.douban.com/top250?start={page * 25}&filter=")



    def parse(self, response: HtmlResponse,**kwargs):
        sel = Selector(response)
        list_items = sel.css('#content > div > div.article > ol > li')
        for list_item in list_items:
            movie_item = MovieItem()
            detail_url = list_item.css('div.hd > a::attr(href)').extract_first() or ' '
            movie_item["title"] = list_item.css('span.title::text').extract_first() or ' '
            movie_item["rating"] = list_item.css('span.rating_num::text').extract_first() or ' '
            movie_item["subject"] = list_item.css('span.inq::text').extract_first() or ' '
            yield Request(url=detail_url,callback=self.parse_detail,
                          cb_kwargs={'item':movie_item})

    def parse_detail(self,response: HtmlResponse,**kwargs):
        movie_item = kwargs['item']
        sel = Selector(response)
        movie_item['duration'] = sel.css('span[property="v:runtime"]::attr(content)').extract_first() or ' '
        movie_item['intro'] = sel.css('span[property="v:summary"]::text').extract_first().strip().replace("\n","") or " "
        yield movie_item





