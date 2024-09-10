
import time

from scrapy import signals, Request
from scrapy.http.response.html import HtmlResponse
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

class Pc17KlistSpiderMiddleware:
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


class Pc17KlistDownloaderMiddleware:
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
            if request.url == "https://www.17k.com/all/book/2_21_0_0_0_0_0_0_1.html":
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

