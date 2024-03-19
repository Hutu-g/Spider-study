from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# 1. 试使用selenium 模拟登录，抓取小说网收藏到书架上的⼩说信息。
# https://www.17k.com/
# 书架：https://user.17k.com/www/bookshelf/
def getWebInfo(url,user_account,user_password,f):
    web = login(url,user_account,user_password)
    catalogs = web.find_elements(By.XPATH, '//*[@id="pageListForm"]/table/tbody/tr/td[2]')
    bookNames = web.find_elements(By.XPATH, '//*[@id="pageListForm"]/table/tbody/tr/td[3]/a')
    lastest = web.find_elements(By.XPATH, '//*[@id="pageListForm"]/table/tbody/tr/td[4]/a')
    updataTime = web.find_elements(By.XPATH, '//*[@id="pageListForm"]/table/tbody/tr/td[5]')
    gray = web.find_elements(By.XPATH, '//*[@id="pageListForm"]/table/tbody/tr/td[6]')
    n = 0
    for catalog, bookName, latest, updateTime, grayItem in zip(catalogs, bookNames, lastest, updataTime, gray):
        n += 1
        print(f"{catalog.text}\t{bookName.text}\t{latest.text}\t{updateTime.text}\t{grayItem.text}")
        f.write(f"{n},{catalog.text},{bookName.text},{latest.text},{updateTime.text},{grayItem.text}\n")

    f.close()
    web.close()

def login(url,user_account,user_password):
    web = webdriver.Chrome()
    web.get(url)
    iframe = web.find_element(By.XPATH,'/html/body/div[4]/div/div/iframe')
    web.switch_to.frame(iframe)
    account_ops = web.find_element(By.XPATH,'/html/body/form/dl/dd[2]/input')
    account_ops.click()
    account_ops.send_keys(user_account)
    password_ops = web.find_element(By.XPATH, '/html/body/form/dl/dd[3]/input')
    password_ops.click()
    password_ops.send_keys(user_password)
    web.find_element(By.XPATH, '//*[@id="protocol"]').click()
    web.find_element(By.XPATH, '/html/body/form/dl/dd[5]/input').click()
    web.switch_to.parent_frame()
    time.sleep(3)
    print("登录成功")

    return web
if __name__ == '__main__':
    user_account = "15060927832"
    user_password = "gaoqiang123"
    url = 'https://user.17k.com/www/bookshelf/'
    f = open("xiaoshuo_01.csv", mode="w", encoding="utf-8")
    getWebInfo(url,user_account,user_password,f)
