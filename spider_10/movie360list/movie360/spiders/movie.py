import scrapy
from scrapy import Selector,Request
from scrapy.http import HtmlResponse

from ..items import Movie360Item
from ..utils.request import SeleniumRequest,SeleniumDetailRequest


class MovieSpider(scrapy.Spider):
    name = "movie"
    allowed_domains = ["video.360kan.com","www.360kan.com"]

    # todo 电影
    # start_urls = ["https://video.360kan.com"]
    def start_requests(self):
        genres = [ '喜剧','爱情','动作','恐怖', '科幻', '剧情', '犯罪', '奇幻', '战争', '悬疑', '动画', '传记',
                  '古装', '历史', '惊悚', '其他']
        for genre in genres:
            for page in range(1, 21):
                yield SeleniumRequest(

                    url=f"https://www.360kan.com/dianying/list?rank=rankhot&cat={genre}&year=&area=&act=&pageno={page}",
                    callback=self.parse)


    # def start_requests(self):
    #     genres = [ '热血', '科幻', '魔幻', '儿歌', '励志', '少儿', '冒险', '搞笑',
    #               '推理', '恋爱', '益智', '幻想','校园','亲子']
    #     for genre in genres:
    #         for page in range(1, 21):
    #             yield SeleniumRequest(
    #                 url=f"https://www.360kan.com/dongman/list?rank=ranklatest&cat={genre}&year=&area=&pageno={page}",
    #                 callback=self.parse)
    def parse(self, response: HtmlResponse, **kwargs):
        sel = Selector(response)
        list_items = sel.css('div.feature-item')
        for list_item in list_items:
            movie_item = Movie360Item()
            movie_item["url"] = "https:" + list_item.css('a.feature-item_href.hover-bright ::attr(href)').extract_first() or ' '
            movie_item["movie_name"] =list_item.css('p.feature-item_tit::text').extract_first() or ' '

            #todo 电影
            movie_item["title_description"] = list_item.css('p.feature-item_subtit::text').extract_first()[:20] or ' '
            # movie_item["title_description"] = "null"
            yield movie_item
