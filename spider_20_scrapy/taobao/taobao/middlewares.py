# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from scrapy.http.response.html import HtmlResponse
from selenium import webdriver
from .utils.request import SeleniumRequest
import time


# useful for handling different item types with a single interface


class TaobaoSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)


class TaobaoDownloaderMiddleware:
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


class sumlenDownloaderMiddleware:
    @classmethod
    def from_crawler(cls, crawler):
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        crawler.signals.connect(s.spider_closed, signal=signals.spider_closed)
        return s

    def spider_opened(self, spider):
        spider.logger.info("当前下载中间件: %s", spider.name)
        options = webdriver.ChromeOptions()
        # options.add_argument('--headless')
        # 去除自动化痕迹
        options.add_experimental_option('excludeSwitches', ['enable-automation'])
        options.add_experimental_option('useAutomationExtension', False)
        options.add_argument("--disable-blink-features=AutomationControlled")
        self.web = webdriver.Chrome(options)
        self.web.implicitly_wait(10)

    def spider_closed(self, spider):
        self.web.close()

    def process_request(self, request, spider):
        if isinstance(request, SeleniumRequest):
            self.web.get(request.url)
            self.web.implicitly_wait(10)
            time.sleep(2)
            # 登录操作 扫码登录
            time.sleep(10)
            self.web.execute_script('window.scrollTo(0, 2000)')
            time.sleep(1)
            self.web.execute_script('window.scrollTo(0, 2321)')
            print("登录成功")
            page_source = self.web.page_source
            return HtmlResponse(url=request.url, request=request, encoding='utf-8', body=page_source)

    def process_response(self, request, response, spider):
        return response

    def process_exception(self, request, exception, spider):
        pass
