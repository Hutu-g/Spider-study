import time

from scrapy import signals, Request
from scrapy.http.response.html import HtmlResponse
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from random import choice
from .settings import USER_AGENT_LIST


class Pc17KdetailSpiderMiddleware:
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


class Pc17KdetailDownloaderMiddleware:
    @classmethod
    def from_crawler(cls, crawler):
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        crawler.signals.connect(s.spider_closed, signal=signals.spider_closed)
        return s

    def spider_opened(self, spider):
        options = Options()
        # 关闭自动化痕迹
        options.add_experimental_option('excludeSwitches', ['enable-automation'])
        options.add_experimental_option('useAutomationExtension', False)
        options.add_argument("--disable-blink-features=AutomationControlled")
        self.web = webdriver.Chrome(options)
        self.web.implicitly_wait(1)

    def spider_closed(self, spider):
        self.web.close()
        pass

    def process_request(self, request, spider):
        if isinstance(request, Request):
            print(f"正在请求{request.url}")
            self.web.get(request.url)
            self.web.implicitly_wait(10)
            time.sleep(2)
            if request.url == "https://www.17k.com/book/3603171.html":
                print("休息60秒")
                time.sleep(60)
            self.web.execute_script('window.scrollTo(0, 2000)')
            time.sleep(2)
            page_source = self.web.page_source
            return HtmlResponse(url=request.url, request=request, encoding='utf-8', body=page_source)

    def process_response(self, request, response, spider):
        return response

    def process_exception(self, request, exception, spider):
        pass


class ProxyDownloaderMiddleware:
    _proxy = (' xxxxxxx ', ' xxxxxxx ')
    def process_request(self, request, spider):
        print("正在进行隧道代理")
        # 用户名密码认证
        username = "xxxxxxx"
        password = " xxxxxxx "
        request.meta['proxy'] = "http://%(user)s:%(pwd)s@%(proxy)s/" % {"user":username, "pwd": password, "proxy": ':'.join(ProxyDownloaderMiddleware._proxy)}
        # 白名单认证
        # request.meta['proxy'] = "http://%(proxy)s/" % {"proxy": proxy}
        request.headers["Connection"] = "close"
        return None
    def process_exception(self, request, exception, spider):
        """捕获407异常"""
        if "'status': 407" in exception.__str__(): # 不同版本的exception的写法可能不一样，可以debug出当前版本的exception再修改条件
            from scrapy.resolver import dnscache
            dnscache.__delitem__(ProxyDownloaderMiddleware._proxy[0]) # 删除proxy host的dns缓存
        return exception


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
