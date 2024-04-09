import time

from chaojiying_Python.chaojiying import Chaojiying_Client
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
import base64
import json
import requests
from common.enums import URL

"""
@Description：工具函数
@Author：hutu-g
@Time：2024/4/2 16:26
"""
class Verify:
    @staticmethod
    def wait(web):
        web.implicitly_wait(10)
        time.sleep(2)

    @staticmethod
    def text_position_verify(web, img,picName,xpath_url):
        width = img.size.get('width')
        height = img.size.get('height')
        chaojiying = Chaojiying_Client(URL.xss["userName"], URL.xss["password"], '946497')
        im = open(picName, 'rb').read()
        yzm = chaojiying.PostPic(im, Chao.code["text_position"])['pic_str']
        for p in yzm.split("|"):
            x, y = p.split(",")
            x = int(x)
            y = int(y)
            ActionChains(web).move_to_element_with_offset(img, x - (width / 2), y - (height / 2)).perform()
            ActionChains(web).click().perform()
        Verify.wait(web)
        web.find_element(By.XPATH,xpath_url).click()
        Verify.wait(web)

    @staticmethod
    def slider_verify(uname, pwd, img, typeid):
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


    @staticmethod
    def get_img(web,picName,action,pos_url):
        img = web.find_element(action, pos_url)
        img.screenshot(picName)
        Verify.wait(web)
        return img

class Chao:
    code = {"text_position":9004}