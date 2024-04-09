from selenium import webdriver
import time
from selenium.webdriver.common.by import By

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

def getDetailInfo(web):
    global good_infos, good_brand
    info = ""
    # 下滑网页
    web.execute_script('window.scrollTo(0, 4000)')
    time.sleep(3)
    # 获取信息
    lis = web.find_elements(By.CLASS_NAME, 'p-parameter')
    for li in lis:
        good_brand = li.find_element(By.ID, 'parameter-brand').find_element(By.TAG_NAME, 'li').get_attribute("title")
        good_infos = li.find_element(By.CSS_SELECTOR, '.parameter2.p-parameter-list').find_elements(By.TAG_NAME,'li')
    info = good_brand + ","
    time.sleep(5)
    for good_info in good_infos:
       info = info +  good_info.get_attribute("title") + "|"
    # 数据处理
    info = info.split("|")[:-1]
    info_str = ','.join(info)
    return info_str

def getDetail(com_url_file, com_file_name,cookie_string):

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
        # 获取当前url网站页参数信息
        detail_info = getDetailInfo(web)
        time.sleep(1)
        good_com_file.write(f"{goods_id},{detail_info}\n")
        print(f"正在爬取第{goods_id}条数据:",detail_info)

    good_com_file.close()
    web.close()
def main():
    # 爬取京东任意评论的好评与差评，并写入文件
    # url文件
    com_url_file = "E:/python_project/spider-study/spider_05/jd_common_datas/jd_getList_ludan.csv"
    # 写入文件目录
    com_file_name = "E:/python_project/spider-study/spider_05/jd_common_datas/jd_getDetail_ludan.csv"
    # 令牌信息
    cookie_string = 'unpl=JF8EAI5nNSttWEpRUklREhBDS1lUW18JTURROm4DV1lZT10MT1AaQER7XlVdWBRKFR9uZBRUXVNOVQ4fCysSEXteXV5tC0oXAG5lBFJcWUtkNRgCKxsgT1VcV18NSRYFX2Y1U21dS1YEHwIYFBVKWWRuVQhDFgFpVwRkXGgJAFkbBhsRFAZZXFZUCk4VAmlXBGRe; shshshfpa=8413f064-1cd6-7bf2-f0e3-24d846e1c9e9-1709350858; shshshfpx=8413f064-1cd6-7bf2-f0e3-24d846e1c9e9-1709350858; __jdu=599834307; TrackID=1H2ACJ90fzHUT3uy_qQOnujPdYEww5W-zqW-lOx2rJmjqIRR-LBgwKqWb-wPAh5Niz858opxA4B-JYJxbOX-IJ8S5DuoOScbklR1dFxu5opgZQWMtO_n6IlPDEo7expnT; __jdv=76161171|cn.bing.com|-|referral|-|1711433069929; PCSYCityID=CN_350000_350500_0; _pst=%E9%AB%98%E6%AD%A6%E5%83%A7; unick=%E9%AB%98%E6%AD%A6%E5%83%A7; pin=%E9%AB%98%E6%AD%A6%E5%83%A7; thor=156BB3FCAA58EFDFD8E508D6EDA826E39A6AC5B9AA2FE89C176E05E06F4699AA24266F962ECACB4D6576AF260F6801EF2CA5644CBBAEA1383F6AE6050499A258EFE6F13F61C2B34537FBD2E194AEE1559E1F31964EBB161FADD9FFFF718F2DBE9B13EA35E43A180538657B2A938F3E4DBE5384B58234EAC3B20CC8EBE4B8CB55; flash=2_RNutsTa9qzH2brqrjAw2NRpd4WwMsoesjw6xtYiBEYDUCYewPGBxfmfwtUGdLpJTHjNOEBp0LNfj7SL1wvfI71Q5IvKs9lOJcHwwHsGr-pq*; _tp=YoMkdxo1JSncSllsJENeFh1v419bEQffnCC0v9bxd48%3D; pinId=M0r8HpWrzLm_c7SdGnP9uQ; 3AB9D23F7A4B3CSS=jdd03WSIVETWYXULI67GGQX6DP4ZVWU5Z3VZKT4XXVVFKPSLN3UMNB2VPYIORUQLDOFCG3IIB24USRSDZYLY2AUDYG7WK5UAAAAMOPF7FVKQAAAAADFCNZTPHLOVKDYX; _gia_d=1; jsavif=1; jsavif=1; xapieid=jdd03WSIVETWYXULI67GGQX6DP4ZVWU5Z3VZKT4XXVVFKPSLN3UMNB2VPYIORUQLDOFCG3IIB24USRSDZYLY2AUDYG7WK5UAAAAMOPF7FVKQAAAAADFCNZTPHLOVKDYX; qrsc=1; areaId=16; ipLoc-djd=16-1332-0-0; __jda=143920055.599834307.1709350857.1711433070.1711435264.3; __jdb=143920055.6.599834307|3.1711435264; __jdc=143920055; rkv=1.0; shshshfpb=BApXeHGx2eutA5V507pGVRkIqTa_9J3gzBkt0D3ds9xJ1Mnek_4O2; 3AB9D23F7A4B3C9B=WSIVETWYXULI67GGQX6DP4ZVWU5Z3VZKT4XXVVFKPSLN3UMNB2VPYIORUQLDOFCG3IIB24USRSDZYLY2AUDYG7WK5U'
    getDetail(com_url_file, com_file_name,cookie_string)


if __name__ == '__main__':
    main()
