import scrapy
from scrapy import Selector,Request
from scrapy.http import HtmlResponse
from ..items import Game4399Item


class Lastgame4399Spider(scrapy.Spider):
    name = "lastGame4399"
    allowed_domains = ["www.4399.com"]
    # start_urls = ["https://www.4399.com"]

    def start_requests(self):
        for page in range(3):
            if page == 0:
                url = 'https://www.4399.com/flash'
            else:
                url = f'https://www.4399.com/flash/new_{page+1}.htm'
            yield Request(url=url)

    def parse(self, response:HtmlResponse,**kwargs):
        sel = Selector(response)
        lis = sel.css('#skinbody > div.bre.oh > ul > li')
        for li in lis:
            game_item = Game4399Item()
            game_item['name'] = li.css('a > b::text').extract_first() or ""
            game_item['type'] = li.css('em:nth-child(2) > a::text').extract_first() or ""
            game_item['updateTimme'] = li.css('em:nth-child(3)::text').extract_first() or ""
            game_item['detailUrl'] = 'https://www.4399.com/' + li.css('a::attr(href)').extract_first() or ""
            yield game_item


