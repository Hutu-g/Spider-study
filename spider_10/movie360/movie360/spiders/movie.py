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
            yield SeleniumDetailRequest(url=movie_item["url"], callback=self.parse_detail,
                    cb_kwargs={'item': movie_item})
    def parse_detail(self,response: HtmlResponse,**kwargs):
        print("开始爬取详情页")
        movie_item = kwargs['item']
        sel = Selector(response)
        movie_item["type"] = ','.join(sel.css('div.anime-information-item_first').css('span a::text').extract()) or " "
        infos_elements = sel.css('span.anime-information-content')
        # 提取每个 span 元素的文本，并赋值给不同的变量
        infos = [span.css('::text').extract_first().strip() for span in infos_elements]
        movie_item["year"] = infos[0]
        movie_item["area"] = infos[1]
        movie_item["director"] = infos[2]
        movie_item["movie_description"] = infos[4]
        movie_item["peoples"] = ','.join(sel.css('div.anime-information-body > div:nth-child(2) > div:nth-child(2) > span').css('span a::text').extract()) or " "
        # todo 电影
        movie_item["vod_name"] = ','.join(sel.css('div.movie-play-sort').css('span > a::text').extract()) or " "
        # movie_item["vod_name"] = ','.join(sel.css('div.dropdown-menu-content > div::text').extract()) or " "
        yield movie_item
