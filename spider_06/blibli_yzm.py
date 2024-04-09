import time
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from chaojiying_Python.chaojiying import Chaojiying_Client
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from common.enums import URL

"""
@Description：
@Author：hutu-g
@Time：2024/4/2 15:46
"""
"""工具函数"""


def wait(web):
    web.implicitly_wait(10)
    time.sleep(1)
def getyzm_action(web, img):
    width = img.size.get('width')
    height = img.size.get('height')
    chaojiying = Chaojiying_Client(URL.xss["userName"], URL.xss["password"], '946497')
    im = open('blibli.png', 'rb').read()
    yzm = chaojiying.PostPic(im, 9004)['pic_str']
    for p in yzm.split("|"):
        x, y = p.split(",")
        x = int(x)
        y = int(y)
        ActionChains(web).move_to_element_with_offset(img, x - (width / 2), y - (height / 2)).perform()
        ActionChains(web).click().perform()
    wait(web)
    web.find_element(By.CLASS_NAME, 'geetest_commit_tip').click()
    wait(web)


def get_img(web):
    img = web.find_element(By.CLASS_NAME, 'geetest_widget')
    img.screenshot('blibli.png')
    wait(web)
    return img


def login(url, userName, password):
    web = webdriver.Chrome()
    web.get(url)
    web.maximize_window()
    wait(web)
    # 点击登录
    web.find_element(By.CLASS_NAME, 'header-login-entry').click()
    wait(web)
    # 输入账号密码
    from_table = web.find_elements(By.CLASS_NAME, 'form__item')
    for inputs in from_table:
        text = inputs.text
        if text == "账号":
            userName_bnt = inputs.find_element(By.CSS_SELECTOR, 'input')
            userName_bnt.click()
            userName_bnt.send_keys(userName)
        else:
            userPassword_bnt = inputs.find_element(By.CSS_SELECTOR, 'input')
            userPassword_bnt.click()
            userPassword_bnt.send_keys(password)
            wait(web)
    wait(web)
    web.find_element(By.CLASS_NAME, 'btn_primary').click()
    wait(web)
    # 通过验证码
    img = get_img(web)
    getyzm_action(web, img)
    time.sleep(3)
    flag = 1
    while flag:
        try:
            web.find_element(By.XPATH, '/html/body/div[9]/div[2]/div[6]/div/div/div[3]/div/a[2]').click()
        except:
            flag = 0
            print("登录成功")
        img = get_img(web)
        getyzm_action(web, img)

    time.sleep(20)
    web.close()


def main():
    # 登录blibli
    url = URL.blibli["url"]
    userName = URL.blibli["userName"]
    password = URL.blibli["password"]
    login(url, userName, password)


if __name__ == '__main__':
    main()
