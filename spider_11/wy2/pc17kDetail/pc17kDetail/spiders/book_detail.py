import scrapy
from scrapy import Selector, Request
from scrapy.http.response.html import HtmlResponse

from ..items import Pc17KdetailItem
import time

class BookDetailSpider(scrapy.Spider):
    name = "book_detail"
    allowed_domains = ["www.17k.com"]
    global error
    error = open("error.txt", mode="a", encoding='utf8')
    def start_requests(self):
        file = open("book_list.csv", mode="r", encoding='utf8')
        datas = file.readlines()
        for line in datas:
            try:
                detail_url = line.split(',')[2]
                id = line.split(',')[3]
            except:
                continue
            try:
                yield Request(
                    url=detail_url,
                    callback=self.parse,
                    cb_kwargs={'id': id})
            except:
                time.sleep(10)
                error.write(f"列表页请求异常，当前条数为{id}\n")
                error.close()

    def parse(self, response: HtmlResponse,**kwargs):
        sel = Selector(response)
        book_item = Pc17KdetailItem()
        book_item["id"] = kwargs['id']
        book_item["intro"] = sel.css("#bookInfo > dd > div:nth-child(1) > p > a::text").extract_first() or " "
        book_item["auth_level"] = sel.css("tbody > tr:nth-child(1) > td:nth-child(2) > span.red ::text").extract_first() or " "
        book_item["week_click"] = sel.css("#weekclickCount ::text").extract_first() or " "
        book_item["month_click"] = sel.css("#monthclickCount ::text").extract_first() or " "
        book_item["week_up"] = sel.css("#hb_week ::text").extract_first() or " "
        book_item["month_up"] = sel.css("#hb_month ::text").extract_first() or " "
        book_item["week_tick"] = sel.css("#flower_week ::text").extract_first() or " "
        book_item["month_tick"] = sel.css("#flower_month ::text").extract_first() or " "
        yield book_item
