# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html
import json
import time

import scrapy
from scrapy import signals, Request
from scrapy.http import HtmlResponse
from selenium import webdriver
from selenium.webdriver.common.by import By


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

    def process_request(self, request: Request, spider):
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
        # crawler.signals.connect(s.spider_closed, signal=signals.spider_closed)
        return cls()

    def process_request(self, request:scrapy.Request, spider):
        #request.cookies = 't=124d136218286caac9b31ae978d28342; _tb_token_=58b53b98a7763; _samesite_flag_=true; 3PcFlag=1713855987990; cookie2=1f61152316d497690d562ea010cfd461; xlly_s=1; unb=2211957752719; lgc=tb2634159185; cancelledSubSites=empty; cookie17=UUpgR1v%2FZzS9LKqjrw%3D%3D; dnk=tb2634159185; tracknick=tb2634159185; _l_g_=Ug%3D%3D; sg=59f; _nk_=tb2634159185; cookie1=VANFkGeXI3esJF5rqCCdGFJ1OhQJ9LgGobSLgsYqs88%3D; sgcookie=E1007UKOkD%2B%2FHu23YVJEeDM47fadVm4HYb19XU83E1txzKYbKo7bbBxhjVhFBiBiPg5V6qDj953gILQY55Fuh5Z9bk4x0Boq3u5IkgjX3p7MfqQ%3D; havana_lgc2_0=eyJoaWQiOjIyMTE5NTc3NTI3MTksInNnIjoiYTQwNjU2MzIyYjMzM2E5NDI1OWY3Mjk3N2QyYzM0MDAiLCJzaXRlIjowLCJ0b2tlbiI6IjE5M25mOEQwbGY4LVdlMzYyQkYyU3N3In0; _hvn_lgc_=0; havana_lgc_exp=1713042077541; cookie3_bak=1f61152316d497690d562ea010cfd461; cookie3_bak_exp=1714115212133; wk_cookie2=16e69fb5cb2a94abd6c844e73a688e58; wk_unb=UUpgR1v%2FZzS9LKqjrw%3D%3D; uc3=vt3=F8dD3e3b7bpgOJ%2Bh2HQ%3D&nk2=F5RHpxdq3hpgA7tw&lg2=UtASsssmOIJ0bQ%3D%3D&id2=UUpgR1v%2FZzS9LKqjrw%3D%3D; csg=a3e73fee; env_bak=FM%2BgndCFxnaS4JaKdxRIp22wWMjhRbiJA5DG3XXZDoQS; skt=5851a34111f79cb9; existShop=MTcxMzg1NjAxMg%3D%3D; uc4=nk4=0%40FY4MtaiA2AUmNIYN2A2obkH7grSCeNc%3D&id4=0%40U2gqyOZmLg%2BryTl2279d%2FXFwWA66LPzp; _cc_=Vq8l%2BKCLiw%3D%3D; mt=ci=14_1; uc1=existShop=false&cookie21=Vq8l%2BKCLiv0MyZ1zjQnMQw%3D%3D&pas=0&cookie15=UtASsssmOIJ0bQ%3D%3D&cookie16=UtASsssmPlP%2Ff1IHDsDaPRu%2BPw%3D%3D&cookie14=UoYfoli5Sa7A5A%3D%3D; JSESSIONID=A210E0E1A9A98F40F6C9BEC5EC570C42; tfstk=f6R-st2WymmkBEkHNUMDYbPsCvumjQLrq38_tMjudnKvRiVnz_DF9HIvYgXlNgVd9eKexHLEzwsBAHIHExcMzU5FOcjKsfYzJ0U2VQCQxEiul6hmjfcMPY_PtEii8Q9mEG7hOa67FEgA-NN7NH65hjsV8wZ5R7gvli7COws5VSafSw2QVwMaHDIbPMVpiCamMUcRqWNBGXWRXUw3OWOAyTd9PiLkrIQReG6cZxcwNnYBZQWqXl1eodKpdHkg3_LBF__MzbFA1U9D9ZAn-JIW4ILXGtUgs6pW2p6wHfyNF9IJhQ6YRWTV9L66p3n8Ug9kDO7fhyhNohjXzQ9x8oTWjgC5ltcsWE6BnQWwZmNR1d8lZptEI-5JRL1A4TdM6YDzjGQ3Fq3YLJW5oaOwYgPSZ08fkG0-9JyF3q7Ajq3YLJW5uZIiy0eULtuV.; isg=BD4-QkxY1M6aqQDqRVhvyfu-j1SAfwL5kSJolehHqgF8i95lUA9SCWRpB1dHtvoR'
        options = webdriver.ChromeOptions()
        # options.add_argument('--headless')
        # 去除自动化痕迹
        options.add_experimental_option('excludeSwitches', ['enable-automation'])
        options.add_experimental_option('useAutomationExtension', False)
        options.add_argument("--disable-blink-features=AutomationControlled")
        web = webdriver.Chrome(options)
        web.get(request.url)
        cookie_string = 't=13abf9e9485e57f571dc875b44751866; thw=cn; miid=1610443652616469931; cna=QgBfHtprgTACAW5W3dTwGAaK; cna=QgBfHtprgTACAW5W3dTwGAaK; sgcookie=E100snhUPtd%2FstQ6Seoo2F0l60E0S%2F9Opg375g6qMOmzXzzWQNixH%2BF%2FIw1lv8IMq3z%2FfwFVIFwleEs%2B49rpOF4BKXY%2B87mw0cOnzLxGJDRdL9Q%3D; uc3=id2=UNN66c8xATJ3PA%3D%3D&nk2=1vYYVz88HIOZH1XO&vt3=F8dD3e5ouCl6Q1BjwPQ%3D&lg2=W5iHLLyFOGW7aA%3D%3D; lgc=%5Cu5012%5Cu8BA1%5Cu65F6%5Cu516B%5Cu89D2%5Cu8857; dnk=%5Cu5012%5Cu8BA1%5Cu65F6%5Cu516B%5Cu89D2%5Cu8857; uc4=nk4=0%401EdQUM9ak0tQgT5KtmiFS9H4bWpRyM4%3D&id4=0%40UgQyfnpmgr5XUq7wPvl4Ml1Jfu9P; tracknick=%5Cu5012%5Cu8BA1%5Cu65F6%5Cu516B%5Cu89D2%5Cu8857; _cc_=URm48syIZQ%3D%3D; _uetsid=6d48f6c0009811ef999d6d87e7e9794f; _uetvid=6d491870009811efbc7ab39d681f6a2b; cookie2=190bc902550b4063c8aac8e4dad2338c; _tb_token_=e11053359e605; hng=GLOBAL%7Czh-CN%7CUSD%7C999; mtop_partitioned_detect=1; _m_h5_tk=14e79887b7692d3636bd77890e0bd788_1713793373866; _m_h5_tk_enc=cf7de36019e0b801b64515664e92747b; xlly_s=1; tfstk=f626rAt47FYsmarIofIEdMSxqrMbhP6y1niYqopwDAH9krZbJ-lxu14jGrznMRkabytgdz92QNfgDKMqHa7PUTrMjxDAzF0uKquimk3YlRYZ9lDmHw-eH_W7jzgzn0fjMMMK0cgxHfdTvMiZDxptMddpJ2mxHqUx6XnKj0m9Xddtvjy6Vm1sSl_2FG6_sFDzX297xJi9U46oRKpbdcZiylIkHKeIffw4TPMIBfPYqb2act9nQuNKp0rGCpM8X0aZ8zBJdvEUvrlutZvrtywjaRhMDCEQhVG8BXtfqkHKDrhbta9rfAPINRNGmeETzVN-Io-57kG7ObmK9nOtQ7rznbeOCU0EZmaZ8zBJdvhA4-prPTIpGHGkhDgPAMODgXNeoyW8jszI6DmsTMsBWSctxDgPAMODifnnf0SCAFFc.; isg=BOLiXXma8BuMde-5TqgK3WE3M2hEM-ZNnVYEOSx7_dUA_4J5FMQQXf19KzsDaV7l'
        cookies = []  # 用于添加到driver内的cookies列表
        for cookie in cookie_string.split(';'):
            name = cookie.split('=')[0].strip()
            value = cookie.split('=')[1].strip()
            domain = '.taobao.com'
            cookies.append({
                "name": name,
                "value": value,
                "domain": domain
            })
        for cookie in cookies:
            web.add_cookie(cookie)
        web.refresh()
        web.execute_script('window.scrollTo(0, 5500)')
        time.sleep(1)
        data = web.page_source
        web.close()

        return HtmlResponse(url=request.url,body= data,request=request,encoding='utf8')

    def process_response(self, request, response, spider):
        return response

    def process_exception(self, request, exception, spider):
        pass

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)
