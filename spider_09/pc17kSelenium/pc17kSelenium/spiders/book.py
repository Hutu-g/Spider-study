from scrapy import Selector
import scrapy
from scrapy.http import HtmlResponse
from ..items import Pc17KseleniumItem

from ..utils.request import SeleniumRequest

class BookSpider(scrapy.Spider):
    name = "book"
    allowed_domains = ["www.17k.com"]
    # start_urls = ["https://www.17k.com"]

    def start_requests(self):
        yield SeleniumRequest(url="https://user.17k.com/www/bookshelf/",callback=self.parse)

    def parse(self, response:HtmlResponse,**kwargs):
        sel = Selector(response)

        lis = sel.css('#pageListForm > table > tbody > tr')
        item = Pc17KseleniumItem()
        for li in lis:
            item["type"] = li.css('td.catalog.gray::text').extract_first() or ""
            item["name"] = li.css('td.bookName > a::text').extract_first() or ""
            item["updatetime"] = li.css('td:nth-child(5)::text').extract_first() or ""
            item["author"] = li.css('td.gray::text').extract_first() or ""
            yield item
