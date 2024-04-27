import scrapy
from scrapy import Selector, Request
from scrapy.http import HtmlResponse

from ..items import LianjiaItem


class BjlianjiaSpider(scrapy.Spider):
    name = "bjlianjia"
    allowed_domains = ["bj.lianjia.com"]

    # start_urls = ["https://bj.lianjia.com"]

    def start_requests(self):
        for page in range(1, 4):
            yield Request(url=f"https://bj.lianjia.com/ershoufang/pg{page}/")

    def parse(self, response):
        sel = Selector(response)
        lis = sel.css('#content > div.leftContent > ul > li')
        'div.info.clear > div.title > a'
        for li in lis:
            lianjian_item = LianjiaItem()
            lianjian_item['title'] = li.css('div.info.clear > div.title > a::text').extract_first() or ""
            lianjian_item['position'] = li.css('div.flood > div > a:nth-child(2)::text').extract_first() or ""
            infos = li.css('div.address > div.houseInfo::text').extract_first().strip().split("|")
            print(infos)

            lianjian_item['huxing'] = infos[0]
            lianjian_item['mianji'] = infos[1]
            lianjian_item['chaoxiang'] = infos[2]
            lianjian_item['zhangxiu'] = infos[3]
            lianjian_item['louceng'] = infos[4]
            if len(infos) == 7:
                lianjian_item['nianfen'] = infos[5]
                lianjian_item['jiegou'] = infos[6]
            else:
                lianjian_item['nianfen'] = "null"
                lianjian_item['jiegou'] = infos[5]
            yield lianjian_item
