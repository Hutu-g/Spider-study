from selenium import webdriver
import time
from selenium.webdriver.common.by import By
import mongo
from common.enums import URL
"""
@Description：
@Author：hutu-g
@Time：2024/3/26 14:13
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


def getData(jd_f_name):
    file = open(jd_f_name, mode="r", encoding='utf8')
    datas = file.readlines()
    return datas

def getGoodCom(web,pages):
    # 下滑网页
    web.execute_script('window.scrollTo(0, 4000)')
    time.sleep(3)
    # 点击商品评论 随后点击只看当前评价 点击好评
    web.find_element(By.XPATH, '//*[@id="detail"]/div[1]/ul/li[5]').click()
    time.sleep(3)
    web.find_element(By.XPATH, '//*[@id="comment"]/div[2]/div[2]/div[1]/ul/li[9]/label').click()
    time.sleep(3)
    web.find_element(By.XPATH,'//*[@id="comment"]/div[2]/div[2]/div[1]/ul/li[5]/a').click()
    time.sleep(1)
    # 下滑一段网页
    flat_page = 1
    count = ""
    # 循环爬取评论
    while flat_page <= pages :
        counts = web.find_elements(By.XPATH, '//*[@id="comment-4"]/div/div[2]/p')
        web.execute_script('window.scrollTo(0, 3000)')
        time.sleep(1)
        for item in counts:
            count += item.text.replace("\n", ",").strip() + "|"
        try:
            iscom = web.execute_script(
                'return document.getElementsByClassName("ui-pager-next")[1].getAttribute("href") == "#comment"')
            if iscom:
                web.execute_script('document.getElementsByClassName("ui-pager-next")[1].click()')
                flat_page += 1
                time.sleep(3)
            else:
                print("没有下一页")
                break
        except :
            print("翻页发生异常:")
            if len(count.split("|")) - 1 == 0:
                count = "null"
            else:
                count = count.split("|")[:-1]
            return count
    if len(count.split("|")) - 1 == 0:
        count = "null"
    else:
        count = count.split("|")[:-1]
    return count

def getBadCom(web,pages):
    # 下滑网页
    web.execute_script('window.scrollTo(0, 4000)')
    time.sleep(3)
    # 点击商品评论 随后点击只看当前评价 点击好评
    web.find_element(By.XPATH, '//*[@id="detail"]/div[1]/ul/li[5]').click()
    time.sleep(3)
    try:
        web.find_element(By.XPATH, '//*[@id="comment"]/div[2]/div[2]/div[1]/ul/li[9]/label').click()
    except:
        time.sleep(5)
        web.find_element(By.XPATH, '//*[@id="comment"]/div[2]/div[2]/div[1]/ul/li[9]/label').click()
    time.sleep(3)
    web.find_element(By.XPATH, '//*[@id="comment"]/div[2]/div[2]/div[1]/ul/li[7]/a').click()
    time.sleep(1)
    # 下滑一段网页
    flat_page = 1
    count = ""
    # 循环爬取评论
    while flat_page <= pages:
        counts = web.find_elements(By.XPATH, '//*[@id="comment-6"]/div/div[2]/p')
        web.execute_script('window.scrollTo(0, 3000)')
        time.sleep(1)
        for item in counts:
            count += item.text.replace("\n", ",").strip() + "|"
        try:
            iscom = web.execute_script(
                'return document.getElementsByClassName("ui-pager-next")[1].getAttribute("href") == "#comment"')
            if iscom:
                web.execute_script('document.getElementsByClassName("ui-pager-next")[1].click()')
                flat_page += 1
                time.sleep(3)
            else:
                print("没有下一页")
                break
        except:
            print("翻页发生异常:")
            if len(count.split("|")) - 1 == 0:
                count = "null"
            else:
                count = count.split("|")[:-1]
            return count
    if len(count.split("|")) - 1 == 0:
        count = "null"
    else:
        count = count.split("|")[:-1]
    return count
def getComment(com_url_file, com_file_name,cookie_string,pages):
    web = webdriver.Chrome()
    datas = getData(com_url_file)
    good_com_file = open(com_file_name, mode="a", encoding='utf8')
    for line in datas:
        # 登录当前url网站设置cookies
        goods_id = line.split(',')[0]
        goods_url = line.split(',')[3]
        web.get(goods_url)
        web.implicitly_wait(10)
        time.sleep(1)
        setCookies(web,cookie_string)
        web.get(goods_url)
        web.implicitly_wait(10)
        time.sleep(4)
        # 获取当前url网站页评论
        good_com = getGoodCom(web,pages)
        web.refresh()
        time.sleep(3)
        bad_com = getBadCom(web,pages)
        good_com_file.write(f"{goods_id},{good_com},{bad_com}\n")
        print(f"正在第{goods_id}条数据")
        print("  好评：===============================================================", good_com)
        print("  差评：>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>", bad_com)

        db = mongo.get_db("jingdong")
        house_dist = {"goods_id": goods_id,"good_com": good_com, "bad_com": bad_com}
        mongo.add_one(db, "comments", house_dist)
        print("写入成功")

    good_com_file.close()
    web.close()
def main():
    # 爬取京东任意评论的好评与差评，并写入文件
    # url文件
    com_url_file = "E:/python_project/spider-study/spider_08/datas/jd_getList_yundongtaozhuang.csv"
    # 写入文件目录
    com_file_name = "E:/python_project/spider-study/spider_08/datas/jd_getCom_yundongtaozhuang.csv"
    # 令牌信息
    cookie_string = URL.jingdong['cookies']
    # 爬取页数
    pages = 2
    getComment(com_url_file, com_file_name,cookie_string,pages)


if __name__ == '__main__':
    main()
