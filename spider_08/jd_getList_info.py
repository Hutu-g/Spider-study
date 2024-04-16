from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from common.enums import URL
"""
@Description：
@Author：hutu-g
@Time：2024/3/27 21:51
"""
def setCookies(web, cookie_string):
    # cookie_string 是登录京东以后的 cookie
    domain1 = '.jd.com'  # 主域名
    domain2 = '.jd.hk'  # 备用域名
    # 分割cookie字符串并创建cookie字典
    for cookie in cookie_string.split(';'):
        name, value = cookie.split('=', 1)  # 使用split第二参数避免切割错误
        cookie_dict = {
            "name": name.strip(),
            "value": value.strip(),
            "domain": domain1  # 首先尝试主域名
        }
        # 尝试添加cookie到web driver
        try:
            web.add_cookie(cookie_dict)
        except:
            # 如果发生异常，更改cookie的domain为备用域名并重新尝试添加
            cookie_dict["domain"] = domain2
            try:
                web.add_cookie(cookie_dict)
            except :
                # 如果再次失败，打印错误消息
                print("添加cookie失败")


def saveList(url,cookie_string,jd_listFile_name,list_page):
    jd_fileList = open(jd_listFile_name, mode="a", encoding='utf8')
    global goods_id
    goods_id = 0
    url = url + "&isList=0&page="
    web = webdriver.Chrome()
    for page in range(1, list_page * 2, 2):
        urls = url + f"{page}"
        web.get(urls)
        web.implicitly_wait(10)
        time.sleep(1)
        setCookies(web,cookie_string)
        web.get(url)
        time.sleep(3)
        web.execute_script('window.scrollTo(0, 3000)')
        time.sleep(3)
        lis = web.find_elements(By.CLASS_NAME, 'gl-i-wrap')
        for li in lis:
            goods_id += 1
            good_prices = li.find_element(By.CLASS_NAME, 'p-price').find_element(By.TAG_NAME,'i').text

            good_titles = li.find_element(By.CSS_SELECTOR, '.p-name.p-name-type-2').find_element(By.TAG_NAME,'em').text.replace("\n", "").strip()

            good_urls = li.find_element(By.CSS_SELECTOR, '.p-name.p-name-type-2').find_element(By.TAG_NAME,'a').get_attribute("href")
            jd_fileList.write(f"{goods_id},{good_titles},{good_prices},{good_urls}\n")
            print(f"{goods_id}\t{good_titles}\t{good_prices}\t{good_urls}\t")
    web.close()
    jd_fileList.close()
def main():
    # 爬取多少页列表信息
    list_page = 2
    # 列表信息文件名
    jd_listFile_name = "E:/python_project/spider-study/spider_08/datas/jd_getList_yundongtaozhuang.csv"
    # 将搜索url复制到这里
    url = f'https://search.jd.com/Search?keyword=%E8%BF%90%E5%8A%A8%E5%A5%97%E8%A3%85&enc=utf-8&wq=%E8%BF%90%E5%8A%A8%E5%A5%97%E8%A3%85&pvid=6bbc098c8b6e4cd0ad961361bb508d06'
    # 令牌信息
    cookie_string = URL.jingdong['cookies']
    # 获取jd任意搜索列表页信息
    saveList(url,cookie_string,jd_listFile_name,list_page)
if __name__ == '__main__':
    main()
