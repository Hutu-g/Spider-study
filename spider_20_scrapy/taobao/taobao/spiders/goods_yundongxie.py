import scrapy


class GoodsYundongxieSpider(scrapy.Spider):
    name = "goods_yundongxie"
    allowed_domains = ["www.taobao.com"]
    start_urls = ["https://www.taobao.com"]

    def parse(self, response):
        pass
