"""
@Description：
@Author：hutu-g
@Time：2024/4/16 22:56
"""
from selenium import webdriver
import time
from selenium.webdriver.common.by import By
import mongo
from mysql import DBHelper


def login(web):
    web.find_element(By.CSS_SELECTOR, ".btn-login.ml1.tb-bg.weight").click()
    mytime(web)
    web.switch_to.window(web.window_handles[-1])
    # 扫码登录
    time.sleep(10)
    web.close()
    web.switch_to.window(web.window_handles[0])


def mytime(web):
    web.implicitly_wait(10)
    time.sleep(1)


def getDetail(url_element, web,tb_detailList):
    url_element.click()
    web.switch_to.window(web.window_handles[-1])
    mytime(web)
    try:
        captcha_element = web.find_element(By.CLASS_NAME, 'baxia-dialog-close')
        captcha_element.click()
    except:
        pass
    shop, isZY, goods_brand, madein, goods_power, nxdegree, area, work_way, color = "", "非自营", "", "", "", "", "", "", ""
    # 是否自营
    current_url = web.current_url.split("?")[0]
    if "tmall" in current_url:
        isZY = "自营"
    web.execute_script('window.scrollTo(0, 2000)')
    # 店铺名
    shop = web.find_element(By.CLASS_NAME, "ShopHeader--title--2qsBE1A").text
    # 其他信息
    infos = web.find_elements(By.CLASS_NAME, 'Attrs--attr--33ShB6X')
    mess = ""
    for info in infos:
        mess = mess + info.text.replace(",", "") + ","
    for info in mess.split(","):
        if "品牌" in info:
            goods_brand = info.split("：")[1]
        if "产地" in info:
            madein = info.split("：")[1]
        if "功率" in info:
            goods_power = info.split("：")[1]
        if "能效" in info:
            nxdegree = info.split("：")[1]
        if "面积" in info:
            area = info.split("：")[1]
        if "工作方式" in info:
            work_way = info.split("：")[1]
        if "颜色" in info:
            color = info.split("：")[1]
    print(goods_id, shop, isZY, goods_brand, madein, goods_power, nxdegree, area, work_way, color)
    tb_detailList.write(f"{goods_id},{shop},{isZY},{goods_brand},{madein},{goods_power},{nxdegree},{area},{work_way},{color}\n")
    data = goods_id, shop, isZY, goods_brand, madein, goods_power, nxdegree, area, work_way, color
    return data


def writeMonggodb(data):
    goods_id, shop, isZY, goods_brand, madein, goods_power, nxdegree, area, work_way, color = data
    db = mongo.get_db("taobao")
    house_dist = {"goods_id": goods_id, "shop": shop, "isZY": isZY, "good_brand": goods_brand, "madein": madein,
                  "goods_power": goods_power, "nxdegree": nxdegree, "area": area, "work_way": work_way, "color": color}
    mongo.add_one(db, "kongtiao", house_dist)
    print("写入成功")


def writeMysql(data):
    goods_id, shop, isZY, goods_brand, madein, goods_power, nxdegree, area, work_way, color = data
    with DBHelper("spider_db") as db:
        db.insert(
            f"insert into kongtiao(goods_id,shop, isZY, goods_brand, madein, goods_power, nxdegree, area, work_way, color) values ('{goods_id}','{shop}','{isZY}','{goods_brand}','{madein}','{goods_power}','{nxdegree}','{area}','{work_way}','{color}')")
    print("写入成功")


def getList(url, title, list_page, tb_listFile_name,tb_detailFile_name):
    # 文件，网页初始化
    tb_fileList = open(tb_listFile_name, mode="a", encoding='utf8')
    tb_detailList = open(tb_detailFile_name, mode="a", encoding='utf8')
    global goods_id
    goods_id = 0
    options = webdriver.ChromeOptions()
    options.add_argument(
        "--disable-blink-features=AutomationControlled")  # chrome去掉了webdriver痕迹，令navigator.webdriver=false
    web = webdriver.Chrome(options=options)
    web.get(url)
    web.maximize_window()
    mytime(web)
    # 登录
    login(web)
    # 搜索内容
    search = web.find_element(By.CLASS_NAME, 'search-suggest-combobox').find_element(By.TAG_NAME, 'input')
    search.click()
    search.send_keys(title)
    web.find_element(By.CSS_SELECTOR, '.btn-search.tb-bg').click()
    mytime(web)
    # 爬取循环每一页 的每一个商品数据
    while (list_page):
        web.execute_script('window.scrollTo(0, 2000)')
        mytime(web)
        web.execute_script('window.scrollTo(0, 2321)')
        mytime(web)
        # 爬取信息 商品名称：goods_name、价格：price、商品详情页url。
        goods_names = web.find_elements(By.CLASS_NAME, 'Title--title--jCOPvpf')
        prices = web.find_elements(By.CLASS_NAME, 'Price--priceInt--ZlsSi_M')
        goods_urls = web.find_elements(By.CLASS_NAME, 'Card--doubleCardWrapper--L2XFE73')
        for name_element, price_element, url_element in zip(goods_names, prices, goods_urls):
            goods_id += 1
            goods_name = name_element.find_element(By.TAG_NAME, 'span').text
            goods_price = price_element.text
            goods_url = url_element.get_attribute("href")
            # todo 列表页写入csv文件
            tb_fileList.write(f"{goods_id},{goods_name},{goods_price},{goods_url}\n")
            print(goods_id, goods_name, goods_price, goods_url)
            # 爬取详情页信息, 店铺：shop、是否为淘宝自营店：isZY、空调品牌：goods_brand、产地：madein、空调功率：goods_power 、能效等级： nxdegree、适用面积：area、工作方式：work_way、颜色：color。
            detailData = getDetail(url_element, web,tb_detailList)
            # todo 写入monggodb
            # writeMonggodb(detailData)
            # todo 写入mysql
            writeMysql(detailData)
            # 关闭页面
            web.close()
            web.switch_to.window(web.window_handles[0])
        # 控制页数
        list_page -= 1
        web.find_element(By.CSS_SELECTOR,
                         ".next-btn.next-medium.next-btn-normal.next-pagination-item.next-next").click()
        mytime(web)
    # 关闭 文件 浏览器
    web.close()
    tb_fileList.close()
    tb_detailList.close()


def main():
    # 爬取多少页列表信息
    list_page = 2
    # 列表信息文件名
    tb_listFile_name = "E:/python_project/spider-study/spider_08/datas/tb_getList_kongtiao.csv"
    tb_detailFile_name = "E:/python_project/spider-study/spider_08/datas/tb_getdetail_kongtiao.csv"
    # 将搜索url复制到这里
    url = "https://www.taobao.com/"
    title = "空调"
    # 获取
    getList(url, title, list_page, tb_listFile_name,tb_detailFile_name)


if __name__ == '__main__':
    main()
