# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from random import choice
from .settings import USER_AGENT_LIST

class Pc17KSpiderMiddleware:
    @classmethod
    def from_crawler(cls, crawler):
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        return None

    def process_spider_output(self, response, result, spider):
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        pass

    def process_start_requests(self, start_requests, spider):
        for r in start_requests:
            yield r
    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)


class Pc17KDownloaderMiddleware:

    @classmethod
    def from_crawler(cls, crawler):
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        return None

    def process_response(self, request, response, spider):
        return response

    def process_exception(self, request, exception, spider):
        pass
    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)
class MyRandomUserAgentMiddleware:
    def process_request(self, request, spider):
        UA = choice(USER_AGENT_LIST)
        request.headers['User-Agent'] = UA
        print("当前UA为 %s",UA)
        return None
    def process_response(self, request, response, spider):
        return response

    def process_exception(self, request, exception, spider):
        pass
    def spider_opened(self, spider):
        spider.logger.info("中间件为: %s" % spider.name)
