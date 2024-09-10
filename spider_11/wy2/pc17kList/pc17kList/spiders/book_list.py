import scrapy

import scrapy
from scrapy import Selector, Request
from scrapy.http import HtmlResponse

from ..items import Pc17KlistItem


class BookListSpider(scrapy.Spider):
    name = "book_list"
    allowed_domains = ["www.17k.com"]
    def __init__(self):
        super(BookListSpider, self).__init__()
        self.id = 1  # 初始化ID为1
    def start_requests(self, ):
        types = {"21": 334, "24": 322, "3": 334, "22": 176}
        # types = {"21": 2}
        for type, max_page in types.items():
            for page in range(1, max_page + 1):
                yield Request(
                    url=f"https://www.17k.com/all/book/2_{type}_0_0_0_0_0_0_{page}.html",
                    callback=self.parse)
    def parse(self, response: HtmlResponse, **kwargs):
        sel = Selector(response)
        book_lis = sel.css("table > tbody > tr.bg0,table > tbody > tr.bg1")
        for li in book_lis:
            book_item = Pc17KlistItem()
            book_item["id"] = self.id
            self.id += 1
            book_item["type"] = li.css("td.td2 > a::text").extract_first() or " "
            book_item["book_name"] = li.css("td.td3 > span > a ::text").extract_first() or " "
            book_item["latest_chapter"] = li.css("td.td4 > a::text").extract_first() or " "
            book_item["word_count"] = li.css("td.td5 ::text").extract_first().strip() or " "
            book_item["author"] = li.css("td.td6 > a::text").extract_first().strip() or " "
            book_item["update_time"] = li.css("td.td7 ::text").extract_first().strip() or " "
            book_item["state"] = li.css("td.td8 > em ::text").extract_first().strip() or " "
            book_item["detail_url"] = "https:" + li.css("td.td3 > span > a::attr(href)").extract_first().strip() or " "
            yield book_item
