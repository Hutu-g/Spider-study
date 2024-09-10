# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

import base64
import json
import random
import time

import requests
# useful for handling different item types with a single interface
from scrapy import signals
from scrapy.http.response.html import HtmlResponse
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By

from .utils.request import SeleniumRequest, SeleniumDetailRequest


class Movie360SpiderMiddleware:
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


class Movie360DownloaderMiddleware:
    @classmethod
    def from_crawler(cls, crawler):
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        crawler.signals.connect(s.spider_closed, signal=signals.spider_closed)
        return s

    def spider_opened(self, spider):
        options = webdriver.ChromeOptions()
        # options.add_argument('--headless')
        options.add_extension('E:/python_project/spider-study/spider_10/AdGuard.crx')
        # 去除自动化痕迹
        options.add_experimental_option('excludeSwitches', ['enable-automation'])
        options.add_experimental_option('useAutomationExtension', False)
        options.add_argument("--disable-blink-features=AutomationControlled")
        self.web = webdriver.Chrome(options)
        self.web.implicitly_wait(1)
        self.web.execute_script('window.open("","_blank");')  # 新建一个标签页

    def spider_closed(self, spider):
        self.web.close()
        pass


    def get_steps(self,dis):
        # 计算公式：v=v0+at, s=v0t+½at², v²-v0²=2as
        v = 0
        t = 0.2
        steps = []
        current = 0
        mid = dis * 5 / 8
        dis += 10
        while current < dis:
            t = random.randint(1, 4) / 10
            if current < mid:
                a = random.randint(1, 3)
            else:
                a = random.randint(2, 4)
            v0 = v
            s = v0 * t + 0.5 * a * (t ** 2)
            current += s
            steps.append(round(s))
            v = v0 + a * t
        # 超过滑块，回退步数
        temp = 10 + round(current - dis)
        for i in range(5):
            num = -random.randint(1, 3)
            steps.append(num)
            temp += num
        # 位移的补偿
        steps.append(abs(temp)) if temp < 0 else steps.append(-temp)
        return steps

    def slider_verify(self,uname, pwd, img, typeid):
        with open(img, 'rb') as f:
            base64_data = base64.b64encode(f.read())
            b64 = base64_data.decode()
        data = {"username": uname, "password": pwd, "typeid": typeid, "image": b64}
        result = json.loads(requests.post("http://api.ttshitu.com/predict", json=data).text)
        if result['success']:
            return result["data"]["result"]
        else:
            # ！！！！！！！注意：返回 人工不足等 错误情况 请加逻辑处理防止脚本卡死 继续重新 识别
            return result["message"]
        return ""

    def process_request(self, request, spider):
        if isinstance(request, SeleniumRequest):
            self.web.switch_to.window(self.web.window_handles[0])
            self.web.get(request.url)
            self.web.implicitly_wait(1)
            time.sleep(1)
            # todo 电影
            # if request.url == 'https://www.360kan.com/dianying/list?rank=rankhot&cat=%E5%96%9C%E5%89%A7&year=&area=&act=&pageno=1':
            if request.url == "https://www.360kan.com/dongman/list?rank=ranklatest&cat=%E7%83%AD%E8%A1%80&year=&area=&pageno=1":
                print(request.url)
                # 登录操作 账号密码登录
                self.web.find_element(By.CLASS_NAME,"nologin_button").click()
                self.web.implicitly_wait(1)
                userName_input = self.web.find_element(By.XPATH,'//div[contains(@class, "quc-input")]//input[@name="mobile"]')
                userName_input.click()
                userName_input.send_keys("15060927832")
                self.web.find_element(By.CSS_SELECTOR,'.quc-link.quc-get-token').click()
                #验证码
                flag = 1
                while flag:
                    result = self.web.find_element(By.CSS_SELECTOR, "div.captcha-result").text
                    print(f"验证信息为{result}"+ ".")
                    if result == "请正确拼合图片" or result == "":
                        img = self.web.find_element(By.CLASS_NAME,"img-con")
                        time.sleep(1)
                        img.screenshot("movie360.png")
                        length = self.slider_verify("shanshan2023", "shanshan2023", "movie360.png", 33)
                        actions = ActionChains(self.web)
                        actions.click_and_hold(self.web.find_element(By.CLASS_NAME, 'slide-btn')).perform()
                        steps = self.get_steps(float(length) - 8)
                        for x in steps:
                            ActionChains(self.web).move_by_offset(x, random.randint(-5, 5)).perform()
                        time.sleep((random.randint(5, 15) / 1000))
                        actions.release().perform()
                        time.sleep(1)
                    else:
                        break
                # 验证码验证成功后
                very_input = self.web.find_element(By.XPATH,
                                                   '//div[contains(@class, "quc-input")]//input[@name="smscode"]')
                print("请输入验证码:")
                smscode = input()
                very_input.click()
                very_input.send_keys(smscode)
                self.web.find_element(By.CSS_SELECTOR,
                                      '.quc-button-submit.quc-button.quc-button-primary').click()
                self.web.implicitly_wait(1)
                time.sleep(1)

            # time.sleep(10)
            self.web.execute_script('window.scrollTo(0, 1000)')
            time.sleep(1)
            self.web.execute_script('window.scrollTo(0, 1000)')
            time.sleep(1)
            page_source = self.web.page_source
            return HtmlResponse(url=request.url, request=request, encoding='utf-8', body=page_source)
        if isinstance(request, SeleniumDetailRequest):
            print(f"正在请求{request.url}")
            self.web.switch_to.window(self.web.window_handles[1])
            self.web.get(request.url)
            self.web.implicitly_wait(1)
            time.sleep(1)
            self.web.find_element(By.XPATH,'//*[@id="app"]/div[2]/div/div[1]/div[2]/div[1]/div[2]/div[3]/div/span/span[2]').click()
            self.web.implicitly_wait(1)
            page_source = self.web.page_source
            return HtmlResponse(url=request.url, request=request, encoding='utf-8', body=page_source)


    def process_response(self, request, response, spider):
        return response

    def process_exception(self, request, exception, spider):
        pass
