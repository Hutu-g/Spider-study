import scrapy
from scrapy import Selector
from scrapy.http import HtmlResponse

from ..items import TaobaoItem


class GoodsYundongxieSpider(scrapy.Spider):
    name = "goods_yundongxie"
    allowed_domains = ["www.taobao.com"]

    def start_requests(self):
        for page in range(2):
            yield scrapy.Request(url=f"https://s.taobao.com/search?commend=all&ie=utf8&initiative_id=tbindexz_20170306&page={page+1}&q=%E7%A9%BA%E8%B0%83&tab=all")
    def parse(self, response:HtmlResponse,**kwargs):
        sel = Selector(response)
        lis = sel.css('div.Content--contentInner--QVTcU0M')
        for li in lis:
            taobao_item = TaobaoItem()
            taobao_item['title'] = li.css('div.Title--title--jCOPvpf > span::text').extract_first() or ""
            taobao_item['price'] = li.css('span.Price--priceInt--ZlsSi_M::text').extract_first() or ""
            taobao_item['url'] = li.css('a.Card--doubleCardWrapper--L2XFE73::attr(href)').extract_first() or ""
            yield taobao_item

