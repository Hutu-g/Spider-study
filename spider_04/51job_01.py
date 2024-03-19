from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


# 2. 试使用selenium 爬取51 job 关于 "软件工程" 相关的岗位信息，具体爬取数据如下：
# 职位名称、工作地点、工作经验、学历要求和职位信息。
def getWebInfo(url, serch_name, f):
    web = login(url)
    input_ops = web.find_element(By.XPATH, '//*[@id="kwdselectid"]')
    input_ops.click()
    input_ops.send_keys(serch_name)
    input_ops.send_keys(Keys.ENTER)
    time.sleep(2)
    job_names = web.find_elements(By.XPATH,
                                  '//*[@id="app"]/div/div[2]/div/div/div[2]/div/div[2]/div/div[2]/div[1]/div/div[2]/div[1]/span[1]')
    global id
    id = 0
    for job_name in job_names:
        id += 1
        jb_n = job_name.text
        print(f"---------------------正在下载第{id}个，职位名称为" + jb_n + "--------------------")
        time.sleep(1)
        job_name.click()
        parseDetail(web, jb_n, f)

    web.close()


def parseDetail(web, jb_n, f):
    time.sleep(1)
    web.switch_to.window(web.window_handles[-1])
    time.sleep(3)
    # 职位名称、工作地点、工作经验、学历要求和职位信息。
    job_add = web.find_element(By.XPATH, '/html/body/div[2]/div/div[2]/div/div[1]/p').text.split('|')[0].strip()
    job_exe = web.find_element(By.XPATH, '/html/body/div[2]/div/div[2]/div/div[1]/p').text.split('|')[1].strip()
    job_degre = web.find_element(By.XPATH, '/html/body/div[2]/div/div[2]/div/div[1]/p').text.split('|')[2].strip()
    job_infos = web.find_element(By.XPATH, '/html/body/div[2]/div/div[3]/div[1]/div').text.strip().replace("\n", "")
    print(jb_n + "," + job_add + "," + job_exe + "," + job_degre + "," + job_infos)
    f.write(f"{id},{jb_n},{job_exe},{job_degre},{job_infos}\n")

    time.sleep(2)
    web.close()
    web.switch_to.window(web.window_handles[0])
    time.sleep(1)


def login(url):
    options = webdriver.ChromeOptions()
    options.add_argument(
        "--disable-blink-features=AutomationControlled")  # 就是这一行告诉chrome去掉了webdriver痕迹，令navigator.webdriver=false，极其关键
    web = webdriver.Chrome(options=options)
    web.get(url)
    # 手动登录
    time.sleep(15)
    print("登录成功")
    return web


if __name__ == '__main__':
    url = 'https://www.51job.com/'
    serch_name = "软件工程"
    f = open("51job_01.csv", mode="w", encoding="utf-8")
    getWebInfo(url, serch_name, f)
