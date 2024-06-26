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
    list_page = 2
    # 列表信息文件名
    jd_listFile_name = "E:/python_project/spider-study/spider_05/jd_common_datas/jd_getList_yundongtaozhuang.csv"
    # 将搜索url复制到这里
    url = f'https://search.jd.com/Search?keyword=%E8%BF%90%E5%8A%A8%E5%A5%97%E8%A3%85&enc=utf-8&wq=%E8%BF%90%E5%8A%A8%E5%A5%97%E8%A3%85&pvid=6bbc098c8b6e4cd0ad961361bb508d06'
    # 令牌信息
    cookie_string = 'shshshfpa=8413f064-1cd6-7bf2-f0e3-24d846e1c9e9-1709350858; shshshfpx=8413f064-1cd6-7bf2-f0e3-24d846e1c9e9-1709350858; __jdu=599834307; qrsc=3; __jdv=76161171|cn.bing.com|-|referral|-|1713247160681; PCSYCityID=CN_350000_350500_0; TrackID=1-lIU56XPjD9GJ09mmLDZSvPxXB6twZOQMdfkgn3mgzsgmPbVDblQAJrYbcViiDNaBotWQwmesWfjZf5J76l4XRMt9xQWe6q4KRG_ThSsIjaZKP7O6iRRCUxvB2on0xSF; _pst=%E9%AB%98%E6%AD%A6%E5%83%A7; unick=%E9%AB%98%E6%AD%A6%E5%83%A7; pin=%E9%AB%98%E6%AD%A6%E5%83%A7; thor=156BB3FCAA58EFDFD8E508D6EDA826E3FFAE414FA4C2449E8AD5D24FF1DCA77545F6FA72204CAFC745BBE245834A9B8F73EC05FB7FA0D7B0AD0C57B87F3DC1DB23DA36704E775E03D4CB430D33A50E816FDD2FECDFB246C1CAAD94ACE84B348CADB0D9B66A9540C274A59F563F59060F98A62A9D666D244356B38D48396CBBAA; flash=2_WdkzWHd0AABA372dWF-aUAyK_d4aHKyb90E1K83XUIEkOeMZj195Mw3EGj-M835hHu8qL6OXA7kGuSfUv0R1-j09mmKQGlkmok_l7a5TWoD*; _tp=YoMkdxo1JSncSllsJENeFh1v419bEQffnCC0v9bxd48%3D; pinId=M0r8HpWrzLm_c7SdGnP9uQ; jsavif=1; jsavif=1; xapieid=jdd03WSIVETWYXULI67GGQX6DP4ZVWU5Z3VZKT4XXVVFKPSLN3UMNB2VPYIORUQLDOFCG3IIB24USRSDZYLY2AUDYG7WK5UAAAAMO4V6RZEIAAAAADGMX6WVWXHSZLIX; __jda=143920055.599834307.1709350857.1711626623.1713247161.9; __jdb=143920055.6.599834307|9.1713247161; __jdc=143920055; 3AB9D23F7A4B3CSS=jdd03WSIVETWYXULI67GGQX6DP4ZVWU5Z3VZKT4XXVVFKPSLN3UMNB2VPYIORUQLDOFCG3IIB24USRSDZYLY2AUDYG7WK5UAAAAMO4WBYCPIAAAAACWLZRFW3GBPDNMX; shshshfpb=BApXc-heL5utA5V507pGVRkIqTa_9J3gzBkt0D3dv9xJ1Mnek_4O2; rkv=1.0; areaId=16; ipLoc-djd=16-1332-0-0; 3AB9D23F7A4B3C9B=WSIVETWYXULI67GGQX6DP4ZVWU5Z3VZKT4XXVVFKPSLN3UMNB2VPYIORUQLDOFCG3IIB24USRSDZYLY2AUDYG7WK5U'
    # 获取jd任意搜索列表页信息
    saveList(url,cookie_string,jd_listFile_name,list_page)
if __name__ == '__main__':
    main()
