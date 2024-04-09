from selenium import webdriver
import time
from selenium.webdriver.common.by import By
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
    list_page = 3
    # 列表信息文件名
    jd_listFile_name = "E:/python_project/spider-study/spider_05/jd_common_datas/jd_getList_ludan.csv"
    # 将搜索url复制到这里
    url = f'https://search.jd.com/Search?keyword=%E5%8D%A4%E8%9B%8B&enc=utf-8&suggest=8.his.0.0&wq=&pvid=0958c59feeb840f89ab01ebca10fa1ab'
    # 令牌信息
    cookie_string = 'unpl=JF8EAI5nNSttWEpRUklREhBDS1lUW18JTURROm4DV1lZT10MT1AaQER7XlVdWBRKFR9uZBRUXVNOVQ4fCysSEXteXV5tC0oXAG5lBFJcWUtkNRgCKxsgT1VcV18NSRYFX2Y1U21dS1YEHwIYFBVKWWRuVQhDFgFpVwRkXGgJAFkbBhsRFAZZXFZUCk4VAmlXBGRe; shshshfpa=8413f064-1cd6-7bf2-f0e3-24d846e1c9e9-1709350858; shshshfpx=8413f064-1cd6-7bf2-f0e3-24d846e1c9e9-1709350858; __jdu=599834307; TrackID=1H2ACJ90fzHUT3uy_qQOnujPdYEww5W-zqW-lOx2rJmjqIRR-LBgwKqWb-wPAh5Niz858opxA4B-JYJxbOX-IJ8S5DuoOScbklR1dFxu5opgZQWMtO_n6IlPDEo7expnT; __jdv=76161171|cn.bing.com|-|referral|-|1711433069929; PCSYCityID=CN_350000_350500_0; _pst=%E9%AB%98%E6%AD%A6%E5%83%A7; unick=%E9%AB%98%E6%AD%A6%E5%83%A7; pin=%E9%AB%98%E6%AD%A6%E5%83%A7; thor=156BB3FCAA58EFDFD8E508D6EDA826E39A6AC5B9AA2FE89C176E05E06F4699AA24266F962ECACB4D6576AF260F6801EF2CA5644CBBAEA1383F6AE6050499A258EFE6F13F61C2B34537FBD2E194AEE1559E1F31964EBB161FADD9FFFF718F2DBE9B13EA35E43A180538657B2A938F3E4DBE5384B58234EAC3B20CC8EBE4B8CB55; flash=2_RNutsTa9qzH2brqrjAw2NRpd4WwMsoesjw6xtYiBEYDUCYewPGBxfmfwtUGdLpJTHjNOEBp0LNfj7SL1wvfI71Q5IvKs9lOJcHwwHsGr-pq*; _tp=YoMkdxo1JSncSllsJENeFh1v419bEQffnCC0v9bxd48%3D; pinId=M0r8HpWrzLm_c7SdGnP9uQ; 3AB9D23F7A4B3CSS=jdd03WSIVETWYXULI67GGQX6DP4ZVWU5Z3VZKT4XXVVFKPSLN3UMNB2VPYIORUQLDOFCG3IIB24USRSDZYLY2AUDYG7WK5UAAAAMOPF7FVKQAAAAADFCNZTPHLOVKDYX; _gia_d=1; jsavif=1; jsavif=1; xapieid=jdd03WSIVETWYXULI67GGQX6DP4ZVWU5Z3VZKT4XXVVFKPSLN3UMNB2VPYIORUQLDOFCG3IIB24USRSDZYLY2AUDYG7WK5UAAAAMOPF7FVKQAAAAADFCNZTPHLOVKDYX; qrsc=1; areaId=16; ipLoc-djd=16-1332-0-0; __jda=143920055.599834307.1709350857.1711433070.1711435264.3; __jdb=143920055.6.599834307|3.1711435264; __jdc=143920055; rkv=1.0; shshshfpb=BApXeHGx2eutA5V507pGVRkIqTa_9J3gzBkt0D3ds9xJ1Mnek_4O2; 3AB9D23F7A4B3C9B=WSIVETWYXULI67GGQX6DP4ZVWU5Z3VZKT4XXVVFKPSLN3UMNB2VPYIORUQLDOFCG3IIB24USRSDZYLY2AUDYG7WK5U'
    # 获取jd任意搜索列表页信息
    saveList(url,cookie_string,jd_listFile_name,list_page)
if __name__ == '__main__':
    main()
