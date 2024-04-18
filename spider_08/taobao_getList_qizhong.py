

import time

from selenium import webdriver
from selenium.webdriver.common.by import By

import mongo
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
def getDetail(url_element,web):
    url_element.click()
    web.switch_to.window(web.window_handles[-1])
    mytime(web)
    try:
        captcha_element = web.find_element(By.CLASS_NAME, 'baxia-dialog-close')
        captcha_element.click()
    except:
        pass

    shop, isZY, goods_brand, close_way, card_price, listing_time, up_height, sex, isMarket = "", "非自营", "", "", "", "", "", "", ""
    # 是否自营
    current_url = web.current_url.split("?")[0]
    if "tmall" in current_url:
        isZY = "自营"
    web.execute_script('window.scrollTo(0, 2000)')
    # 店铺
    shop = web.find_element(By.CLASS_NAME, "ShopHeader--title--2qsBE1A").text
    # 其他信息
    infos = web.find_elements(By.CLASS_NAME, 'Attrs--attr--33ShB6X')
    mess = ""
    for info in infos:
        mess = mess + info.text.replace(",", "") + ","
    # 6.数据完整性，数据无乱序、串行、串列情
    for info in mess.split(","):
        if "品牌" in info:
            goods_brand = info.split("：")[1]
        if "闭合方式" in info:
            close_way = info.split("：")[1]
        if "吊牌价" in info:
            card_price = info.split("：")[1]
        if "上市时间" in info:
            listing_time = info.split("：")[1]
        if "鞋帮高度" in info:
            up_height = info.split("：")[1]
        if "性别" in info:
            sex = info.split("：")[1]
        if "是否商场同款" in info:
            isMarket = info.split("：")[1]
    print(goods_id, shop, isZY, goods_brand, close_way, card_price, listing_time, up_height, sex, isMarket)
    data = goods_id, shop, isZY, goods_brand, close_way, card_price, listing_time, up_height, sex, isMarket
    return data
def writeMonggodb(data):
    goods_id, shop, isZY, goods_brand, close_way, card_price, listing_time, up_height, sex, isMarket = data
    db = mongo.get_db("taobao")
    house_dist = {"goods_id": goods_id, "shop": shop, "isZY": isZY, "good_brand": goods_brand, "close_way": close_way,
                  "card_price": card_price, "listing_time": listing_time, "up_height": up_height, "sex": sex, "isMarket": isMarket}
    mongo.add_one(db, "goodsinfo", house_dist)
    print("详情页写入mongodb成功")
def writeCSV(data,tb_detailList):
    goods_id, shop, isZY, goods_brand, close_way, card_price, listing_time, up_height, sex, isMarket = data
    tb_detailList.write(f"{goods_id},{shop},{isZY},{goods_brand},{close_way},{card_price},{listing_time},{up_height},{sex},{isMarket}\n")

def getList(url,title,list_page,tb_listFile_name,tb_detailFile_name):
    # 文件，网页初始化
    tb_fileList = open(tb_listFile_name, mode="a", encoding='utf8')
    tb_detailList = open(tb_detailFile_name, mode="a", encoding='utf8')
    global goods_id
    goods_id = 0
    options = webdriver.ChromeOptions()
    options.add_argument(
        "--disable-blink-features=AutomationControlled")  #chrome去掉了webdriver痕迹，令navigator.webdriver=false
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
    while(list_page):
        web.execute_script('window.scrollTo(0, 2000)')
        mytime(web)
        web.execute_script('window.scrollTo(0, 2321)')
        mytime(web)
        # 1.爬取信息 商品名称：goods_name、价格：price、商品详情页url。
        goods_names = web.find_elements(By.CLASS_NAME, 'Title--title--jCOPvpf')
        prices = web.find_elements(By.CLASS_NAME, 'Price--priceInt--ZlsSi_M')
        goods_urls = web.find_elements(By.CLASS_NAME, 'Card--doubleCardWrapper--L2XFE73')
        for name_element, price_element, url_element in zip(goods_names, prices, goods_urls):
            goods_id += 1
            goods_name = name_element.find_element(By.TAG_NAME, 'span').text
            goods_price = price_element.text
            goods_url = url_element.get_attribute("href")
            # 4. 列表页写入csv文件
            tb_fileList.write(f"{goods_id},{goods_name},{goods_price},{goods_url}\n")
            # 5. 列表页写入monggodb
            db = mongo.get_db("taobao")
            house_dist = {"goods_id": goods_id, "goods_name": goods_name, "goods_price": goods_price, "goods_url": goods_url,}
            mongo.add_one(db, "goodslist", house_dist)
            print(goods_id,goods_name, goods_price, goods_url)
            # 2.爬取详情页信息,
            # 店铺:shop、是否为淘宝自营店:isZY、品牌:goods brand、闭合方式:close way、
            # 鞋帮高度:wpp height、<吊牌价:card price、上市时间:listing time、isMarket。
            # 性别:sex、是否商场同款
            detailData = getDetail(url_element, web)
            # 4. 详情页写入csv文件
            writeCSV(detailData,tb_detailList)
            # 5. 详情页写入monggodb
            writeMonggodb(detailData)


            # 关闭页面
            web.close()
            web.switch_to.window(web.window_handles[0])
        # 控制页数
        list_page -= 1
        web.find_element(By.CSS_SELECTOR,".next-btn.next-medium.next-btn-normal.next-pagination-item.next-next").click()
        mytime(web)
    # 关闭 文件 浏览器
    web.close()
    tb_detailList.close()
    tb_fileList.close()
def main():
    # 爬取2页列表信息
    list_page = 2
    # 列表信息文件名
    tb_listFile_name = "E:/python_project/spider-study/spider_09qizhong/goodsList.csv"
    tb_detailFile_name = "E:/python_project/spider-study/spider_09qizhong/goodsinfo.csv"

    # 将搜索url复制到这里
    url = "https://www.taobao.com/"
    title = "运动鞋"
    # 获取
    getList(url,title,list_page,tb_listFile_name,tb_detailFile_name)
if __name__ == '__main__':
    main()












