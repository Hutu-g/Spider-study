from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

#测试环境
if __name__ == '__main__':
    # 爬取百度标题
    driver = webdriver.Chrome()  # 声明浏览器驱动对象
    driver.get('https://www.baidu.com/')
    time.sleep(2)
    titles =driver.find_elements(By.XPATH,'//*[@id="hotsearch-content-wrapper"]/li/a/span[2]')
    for i in titles:
        print(i.text)
    driver.close()