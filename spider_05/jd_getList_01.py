from selenium import webdriver
import time
from selenium.webdriver.common.by import By

"""
@Description：
@Author：hutu-g
@Time：2024/3/26 14:13
"""


def setCookies(web):
    # cookie_string 是登录京东以后的 cookie
    cookie_string = 'unpl=JF8EAI5nNSttWEpRUklREhBDS1lUW18JTURROm4DV1lZT10MT1AaQER7XlVdWBRKFR9uZBRUXVNOVQ4fCysSEXteXV5tC0oXAG5lBFJcWUtkNRgCKxsgT1VcV18NSRYFX2Y1U21dS1YEHwIYFBVKWWRuVQhDFgFpVwRkXGgJAFkbBhsRFAZZXFZUCk4VAmlXBGRe; shshshfpa=8413f064-1cd6-7bf2-f0e3-24d846e1c9e9-1709350858; shshshfpx=8413f064-1cd6-7bf2-f0e3-24d846e1c9e9-1709350858; __jdu=599834307; TrackID=1H2ACJ90fzHUT3uy_qQOnujPdYEww5W-zqW-lOx2rJmjqIRR-LBgwKqWb-wPAh5Niz858opxA4B-JYJxbOX-IJ8S5DuoOScbklR1dFxu5opgZQWMtO_n6IlPDEo7expnT; __jdv=76161171|cn.bing.com|-|referral|-|1711433069929; PCSYCityID=CN_350000_350500_0; _pst=%E9%AB%98%E6%AD%A6%E5%83%A7; unick=%E9%AB%98%E6%AD%A6%E5%83%A7; pin=%E9%AB%98%E6%AD%A6%E5%83%A7; thor=156BB3FCAA58EFDFD8E508D6EDA826E39A6AC5B9AA2FE89C176E05E06F4699AA24266F962ECACB4D6576AF260F6801EF2CA5644CBBAEA1383F6AE6050499A258EFE6F13F61C2B34537FBD2E194AEE1559E1F31964EBB161FADD9FFFF718F2DBE9B13EA35E43A180538657B2A938F3E4DBE5384B58234EAC3B20CC8EBE4B8CB55; flash=2_RNutsTa9qzH2brqrjAw2NRpd4WwMsoesjw6xtYiBEYDUCYewPGBxfmfwtUGdLpJTHjNOEBp0LNfj7SL1wvfI71Q5IvKs9lOJcHwwHsGr-pq*; _tp=YoMkdxo1JSncSllsJENeFh1v419bEQffnCC0v9bxd48%3D; pinId=M0r8HpWrzLm_c7SdGnP9uQ; 3AB9D23F7A4B3CSS=jdd03WSIVETWYXULI67GGQX6DP4ZVWU5Z3VZKT4XXVVFKPSLN3UMNB2VPYIORUQLDOFCG3IIB24USRSDZYLY2AUDYG7WK5UAAAAMOPF7FVKQAAAAADFCNZTPHLOVKDYX; _gia_d=1; jsavif=1; jsavif=1; xapieid=jdd03WSIVETWYXULI67GGQX6DP4ZVWU5Z3VZKT4XXVVFKPSLN3UMNB2VPYIORUQLDOFCG3IIB24USRSDZYLY2AUDYG7WK5UAAAAMOPF7FVKQAAAAADFCNZTPHLOVKDYX; qrsc=1; areaId=16; ipLoc-djd=16-1332-0-0; __jda=143920055.599834307.1709350857.1711433070.1711435264.3; __jdb=143920055.6.599834307|3.1711435264; __jdc=143920055; rkv=1.0; shshshfpb=BApXeHGx2eutA5V507pGVRkIqTa_9J3gzBkt0D3ds9xJ1Mnek_4O2; 3AB9D23F7A4B3C9B=WSIVETWYXULI67GGQX6DP4ZVWU5Z3VZKT4XXVVFKPSLN3UMNB2VPYIORUQLDOFCG3IIB24USRSDZYLY2AUDYG7WK5U'
    cookies = []  # 用于添加到driver内的cookies列表
    for cookie in cookie_string.split(';'):
        name = cookie.split('=')[0].strip()
        value = cookie.split('=')[1].strip()
        domain = '.jd.com'
        cookies.append({
            "name": name,
            "value": value,
            "domain": domain
        })
    for cookie in cookies:
        web.add_cookie(cookie)


def saveList(pages,jd_fileList):
    global goods_id
    goods_id = 0
    web = webdriver.Chrome()
    for page in range(1, pages * 2, 2):
        url = f'https://search.jd.com/Search?keyword=%E5%A9%B4%E5%84%BF%E5%A5%B6%E7%B2%89&qrst=1&wq=%E5%A9%B4%E5%84%BF%E5%A5%B6%E7%B2%89&stock=1&pvid=be3bb731c6d347728f471d92ac39d07b&isList=0&page={page}'
        web.get(url)
        web.implicitly_wait(10)
        time.sleep(1)
        setCookies(web)
        web.get(url)
        time.sleep(5)
        print("登录成功")
        web.execute_script('window.scrollTo(0, 3000)')
        lis = web.find_elements(By.XPATH, '//*[@id="J_goodsList"]/ul/li')
        for li in lis:
            goods_id += 1
            good_prices = li.find_element(By.XPATH, './div/div[2]/strong/i').text
            good_titles = li.find_element(By.XPATH, './div/div[3]/a/em').text.replace("\n", "").replace(" ", "").strip()
            good_urls = li.find_element(By.XPATH, './div/div[1]/a').get_attribute("href")
            jd_fileList.write(f"{goods_id},{good_titles},{good_prices},{good_urls}\n")
            print(f"{goods_id}\t{good_titles}\t{good_prices}\t{good_urls}\t")
    web.close()


def main():
    page = 3
    jd_file_name = "datas/jd_getList_01.csv"
    jd_fileList = open(jd_file_name,mode="a",encoding='utf8')
    saveList(page,jd_fileList)
    jd_fileList.close()


if __name__ == '__main__':
    main()
