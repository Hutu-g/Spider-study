from selenium import webdriver
import time
from chaojiying_Python.chaojiying import Chaojiying_Client
from selenium.webdriver.common.by import By
from common.enums import URL

"""
@Description：
@Author：hutu-g
@Time：2024/4/2 14:39
"""


def getyzm():
    chaojiying = Chaojiying_Client('shanshan2023', 'shanshan2023', '946497')
    im = open('chaojiying.png', 'rb').read()
    yzm = chaojiying.PostPic(im, 1902)['pic_str']
    return yzm


def login(url):
    web = webdriver.Chrome()
    web.get(url)
    web.maximize_window()
    time.sleep(1)
    login_but = web.find_element(By.XPATH, '//*[@id="login-register"]/a')
    login_but.click()
    user = web.find_element(By.XPATH, '//*[@id="user"]')
    user.send_keys(URL.chaojiying["userName"])
    password = web.find_element(By.XPATH, '//*[@id="pass"]')
    password.send_keys(URL.chaojiying["password"])
    web.find_element(By.XPATH, '//*[@id="userone"]/section/form/div[3]/div/img').screenshot("chaojiying.png")
    yzm = getyzm()
    yzm_tex = web.find_element(By.XPATH, '//*[@id="auth"]')
    yzm_tex.click()
    yzm_tex.send_keys(yzm)
    web.find_element(By.XPATH, '//*[@id="userone"]/section/form/div[6]/button').click()
    time.sleep(20)


def mian():
    # 登录超级鹰
    url = "https://www.chaojiying.com/"
    login(url)


if __name__ == '__main__':
    mian()
