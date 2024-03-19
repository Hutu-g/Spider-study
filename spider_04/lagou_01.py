
from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

#爬取拉勾网职业信息
def getWebObject(url):
    web = webdriver.Chrome()
    web.get(url)
    time.sleep(1)
    #todo 手动登录
    web.find_element(By.XPATH, '//*[@id="lg_tbar"]/div[2]/ul/li[1]/a').click()
    web.find_element(By.XPATH, '/html/body/div[3]/div/div[2]/div/div[2]/div/div[2]/div[1]/div[1]/img').click()
    time.sleep(10)

    return web
def getAllPages(web,job_name,endpage):
    web.find_element(By.XPATH ,'//*[@id="lg_tbar"]/div[1]/ul/li[3]/a').click()
    time.sleep(1)
    input_ops = web.find_element(By.XPATH ,'//*[@id="keyword"]')
    input_ops.send_keys(job_name)
    input_ops.send_keys(Keys.ENTER)
    time.sleep(2)
    job_titles = web.find_elements(By.XPATH,'//*[@id="openWinPostion"]')
    global id
    id = 0
    for job_title in job_titles:
        id  = id + 1
        print(f"------------------------------正在爬取第{id}条" + job_title.text + "详情页信息"+"------------------------------")
        job_title.click()
        parseDetail(web)
    web.close()
    print()


def parseDetail(web):
    time.sleep(1)
    web.switch_to.window(web.window_handles[-1])
    #：岗位名称、岗位职责和任职要求。
    job_detail = web.find_element(By.CLASS_NAME, 'job-detail').text
    print(job_detail)
    web.close()
    web.switch_to.window(web.window_handles[0])
    time.sleep(1)


if __name__ == '__main__':
    endpage = 3
    url = 'https://www.lagou.com/'
    job_name = 'python'
    web = getWebObject(url)
    getAllPages(web,job_name,endpage)

