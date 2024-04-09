import time
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from chaojiying_Python.chaojiying import Chaojiying_Client
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from common.enums import URL
from common.utils import Verify
import random

"""
@Description：
@Author：hutu-g
@Time：2024/4/2 22:00
"""

def get_steps(dis):
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

def very(web):
    Verify.wait(web)
    img_name = "zhubajie.png"
    Verify.get_img(web, img_name, By.CSS_SELECTOR, ".geetest_slicebg.geetest_absolute")
    # yzm_img = WebDriverWait(web, 10).until(
    #     EC.presence_of_element_located((By.CSS_SELECTOR, ".geetest_slicebg.geetest_absolute"))
    # )
    # Verify.wait(web)
    # yzm_img.screenshot("zhubajie.png")
    # Verify.wait(web)
    # 获取验证码
    length = Verify.slider_verify(URL.xss["userName"], URL.xss["password"], img_name, 33)
    print(length)
    # 输入验证码
    actions = ActionChains(web)
    actions.click_and_hold(web.find_element(By.CLASS_NAME, 'geetest_slider_button')).perform()

    steps = get_steps(float(length) - 8)

    for x in steps:
        ActionChains(web).move_by_offset(x, random.randint(-5, 5)).perform()
    time.sleep((random.randint(5, 15) / 1000))
    actions.release().perform()
    time.sleep(3)
def while_yzm(web,userName, password):
    Verify.wait(web)
    web.maximize_window()
    # 输入账号密码
    web.find_element(By.XPATH,'//*[@id="utopia_widget_10"]/ul/ol/a/span/img').click()
    Verify.wait(web)
    userName_but = web.find_element(By.XPATH,'//*[@id="username"]')
    userName_but.click()
    userName_but.send_keys(userName)
    Verify.wait(web)
    password_but = web.find_element(By.XPATH, '//*[@id="password"]')
    password_but.click()
    password_but.send_keys(password)
    Verify.wait(web)
    web.find_element(By.XPATH,'//*[@id="accent-protocal"]/div/i/span').click()
    Verify.wait(web)
    # 点击验证码
    web.find_element(By.XPATH,'//*[@id="password-captcha-box"]/div[2]/div[2]/div[1]/div[3]/span[1]').click()
    # 获取验证码图片
    flag = 1
    while flag:
        Verify.wait(web)
        info = web.find_element(By.CLASS_NAME, 'geetest_radar_tip').get_attribute('aria-label')
        # 直接验证成功
        if  info == '验证成功':
            flag = 0
            return flag
        # 正常验证
        elif info == '请完成验证':
            very(web)
            info = web.find_element(By.CLASS_NAME, 'geetest_radar_tip').get_attribute('aria-label')
            flag_re = 0
            if info == '网络不给力':
                flag_re = 0
            elif info == '验证成功':
                flag_re = 0
            else:
                flag_re = 1
                while flag_re:
                    try:
                        web.find_element(By.CLASS_NAME, 'geetest_refresh_1').click()
                    except:
                        flag_re = 0
                    try:
                        very(web)
                    except:
                        break
        # 网络异常
        elif info == '网络不给力':
            web.find_element(By.CLASS_NAME, 'geetest_reset_tip_content').click()
            flag = 1
    return flag

def login(url, userName, password):
    options = webdriver.ChromeOptions()
    options.add_argument(
        "--disable-blink-features=AutomationControlled")  #chrome去掉了webdriver痕迹，令navigator.webdriver=false
    web = webdriver.Chrome(options=options)
    web.get(url)
    # 循环验证码

    flag = while_yzm(web,userName, password)

    if flag == 0:
        web.find_element(By.XPATH,'//*[@id="login"]/div/div[5]/button').click()
        print("登录成功")
    time.sleep(5)
    web.close()






def main():
    url = URL.zhubajie["url"]
    userName = URL.zhubajie["userName"]
    password = URL.zhubajie["password"]
    print(url, userName, password)
    while 1:
        login(url, userName, password)


if __name__ == '__main__':
    main()
