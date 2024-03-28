from selenium import webdriver
import time
from selenium.webdriver.common.by import By

"""
@Description：
@Author：hutu-g
@Time：2024/3/26 14:13
"""


def setCookies(web, domain):
    # cookie_string 是登录京东以后的 cookie
    cookie_string = 'unpl=JF8EAI5nNSttWEpRUklREhBDS1lUW18JTURROm4DV1lZT10MT1AaQER7XlVdWBRKFR9uZBRUXVNOVQ4fCysSEXteXV5tC0oXAG5lBFJcWUtkNRgCKxsgT1VcV18NSRYFX2Y1U21dS1YEHwIYFBVKWWRuVQhDFgFpVwRkXGgJAFkbBhsRFAZZXFZUCk4VAmlXBGRe; shshshfpa=8413f064-1cd6-7bf2-f0e3-24d846e1c9e9-1709350858; shshshfpx=8413f064-1cd6-7bf2-f0e3-24d846e1c9e9-1709350858; __jdu=599834307; TrackID=1H2ACJ90fzHUT3uy_qQOnujPdYEww5W-zqW-lOx2rJmjqIRR-LBgwKqWb-wPAh5Niz858opxA4B-JYJxbOX-IJ8S5DuoOScbklR1dFxu5opgZQWMtO_n6IlPDEo7expnT; __jdv=76161171|cn.bing.com|-|referral|-|1711433069929; PCSYCityID=CN_350000_350500_0; _pst=%E9%AB%98%E6%AD%A6%E5%83%A7; unick=%E9%AB%98%E6%AD%A6%E5%83%A7; pin=%E9%AB%98%E6%AD%A6%E5%83%A7; thor=156BB3FCAA58EFDFD8E508D6EDA826E39A6AC5B9AA2FE89C176E05E06F4699AA24266F962ECACB4D6576AF260F6801EF2CA5644CBBAEA1383F6AE6050499A258EFE6F13F61C2B34537FBD2E194AEE1559E1F31964EBB161FADD9FFFF718F2DBE9B13EA35E43A180538657B2A938F3E4DBE5384B58234EAC3B20CC8EBE4B8CB55; flash=2_RNutsTa9qzH2brqrjAw2NRpd4WwMsoesjw6xtYiBEYDUCYewPGBxfmfwtUGdLpJTHjNOEBp0LNfj7SL1wvfI71Q5IvKs9lOJcHwwHsGr-pq*; _tp=YoMkdxo1JSncSllsJENeFh1v419bEQffnCC0v9bxd48%3D; pinId=M0r8HpWrzLm_c7SdGnP9uQ; 3AB9D23F7A4B3CSS=jdd03WSIVETWYXULI67GGQX6DP4ZVWU5Z3VZKT4XXVVFKPSLN3UMNB2VPYIORUQLDOFCG3IIB24USRSDZYLY2AUDYG7WK5UAAAAMOPF7FVKQAAAAADFCNZTPHLOVKDYX; _gia_d=1; jsavif=1; jsavif=1; xapieid=jdd03WSIVETWYXULI67GGQX6DP4ZVWU5Z3VZKT4XXVVFKPSLN3UMNB2VPYIORUQLDOFCG3IIB24USRSDZYLY2AUDYG7WK5UAAAAMOPF7FVKQAAAAADFCNZTPHLOVKDYX; qrsc=1; areaId=16; ipLoc-djd=16-1332-0-0; __jda=143920055.599834307.1709350857.1711433070.1711435264.3; __jdb=143920055.6.599834307|3.1711435264; __jdc=143920055; rkv=1.0; shshshfpb=BApXeHGx2eutA5V507pGVRkIqTa_9J3gzBkt0D3ds9xJ1Mnek_4O2; 3AB9D23F7A4B3C9B=WSIVETWYXULI67GGQX6DP4ZVWU5Z3VZKT4XXVVFKPSLN3UMNB2VPYIORUQLDOFCG3IIB24USRSDZYLY2AUDYG7WK5U'
    cookies = []  # 用于添加到driver内的cookies列表
    for cookie in cookie_string.split(';'):
        name = cookie.split('=')[0].strip()
        value = cookie.split('=')[1].strip()
        cookies.append({
            "name": name,
            "value": value,
            "domain": domain
        })
    for cookie in cookies:
        web.add_cookie(cookie)


def getData(jd_f_name):
    file = open(jd_f_name, mode="r", encoding='utf8')
    datas = file.readlines()
    return datas


def saveDetail(jd_f_name, jd_df_name,jd_comment_name):
    goods_id, isJD, brand, goods_name, madein, grade, isImport, weight = "", "", "", "", "", "", "", ""
    web = webdriver.Chrome()
    datas = getData(jd_f_name)
    jd_Detail_01 = open(jd_df_name, mode="a", encoding='utf8')
    jd_Detail_Comment = open(jd_comment_name, mode="a", encoding='utf8')
    for line in datas:
        goods_id = line.split(',')[0]
        goods_url = line.split(',')[3]
        web.get(goods_url)
        web.implicitly_wait(10)
        time.sleep(1)
        try:
            domain = '.jd.com'
            setCookies(web, domain)
        except:
            domain = '.jd.hk'
            setCookies(web, domain)
        web.get(goods_url)
        web.implicitly_wait(10)
        time.sleep(5)
        try:
            isJD = web.find_element(By.XPATH, '//*[@id="crumb-wrap"]/div/div[2]/div[2]/div[1]/div/a').text
            if "自营" in isJD:
                isJD = "自营"
            else:
                isJD = "非自营"
        except:
            print("未获取到数据")
        brand = web.find_element(By.XPATH, '//*[@id="parameter-brand"]/li/a').text.strip()
        infos = web.find_element(By.XPATH, '//*[@id="detail"]/div[2]/div[1]/div[1]/ul[2]').text.replace("\n", ",")
        for info in infos.split(","):
            if "商品名称" in info:
                goods_name = info.split("：")[1]
            if "产地" in info:
                madein = info.split("：")[1]
            if "段位" in info:
                grade = info.split("：")[1]
            if "是否进口" in info:
                isImport = info.split("：")[1]
            if "净含量" in info:
                weight = info.split("：")[1]
            time.sleep(1)


        jd_Detail_01.write(f"{goods_id},{isJD},{brand},{goods_name},{madein},{grade},{isImport}\n")

        print(f"正在爬取第{goods_id}条数据，数据为：" + isJD, brand, goods_name, madein, grade, isImport, weight)
        getComment(goods_id, web,jd_Detail_Comment)


    jd_Detail_01.close()
    jd_Detail_Comment.close()
    web.close()


def getComment(goods_id, web, jd_Detail_Comment):
    web.execute_script('window.scrollTo(0, 4000)')
    time.sleep(1)
    web.find_element(By.XPATH, '//*[@id="detail"]/div[1]/ul/li[5]').click()
    time.sleep(5)
    try:
        web.find_element(By.XPATH, '//*[@id="comment"]/div[2]/div[2]/div[1]/ul/li[9]/label').click()
    except Exception as e:
        print("没有加载出显示全部",e)
    time.sleep(3)
    com_all_count = web.find_element(By.XPATH, '//*[@id="comment"]/div[2]/div[2]/div[1]/ul/li[1]/a/em').text.replace(
        "(", "").replace(")", "")
    com_img_count = web.find_element(By.XPATH, '//*[@id="comment"]/div[2]/div[2]/div[1]/ul/li[2]/a/em').text.replace(
        "(", "").replace(")", "")
    com_video_count = web.find_element(By.XPATH, '//*[@id="comment"]/div[2]/div[2]/div[1]/ul/li[3]/a/em').text.replace(
        "(", "").replace(")", "")
    com_add_count = web.find_element(By.XPATH, '//*[@id="comment"]/div[2]/div[2]/div[1]/ul/li[4]/a/em').text.replace(
        "(", "").replace(")", "")
    com_good_count = int(web.find_element(By.XPATH, '//*[@id="comment"]/div[2]/div[2]/div[1]/ul/li[5]/a/em').text.replace(
        "(", "").replace(")", "").replace("+","").replace("万","").replace(".",""))
    com_mid_count = web.find_element(By.XPATH, '//*[@id="comment"]/div[2]/div[2]/div[1]/ul/li[6]/a/em').text.replace(
        "(", "").replace(")", "")
    com_bad_count = int(web.find_element(By.XPATH, '//*[@id="comment"]/div[2]/div[2]/div[1]/ul/li[7]/a/em').text.replace(
        "(", "").replace(")", "").replace("+","").replace("万","").replace(".",""))
    pages = 3
    try:
        web.find_element(By.XPATH, '//*[@id="comment"]/div[2]/div[2]/div[1]/ul/li[5]/a').click()
    except :
        print("好评点击异常",)
    time.sleep(5)
    type = "good"
    try:
        good_count = getCommentinfo(web, pages,type,com_good_count)
    except :
        print("好评获取异常")
        good_count = "None"
    time.sleep(5)
    type = "bad"
    try:
        web.find_element(By.XPATH, '//*[@id="comment"]/div[2]/div[2]/div[1]/ul/li[7]/a').click()
        time.sleep(2)
    except :
        print("差评点击异常")
    try:
        bad_count = getCommentinfo(web, pages, type,com_bad_count)
        time.sleep(5)
    except :
        print("差评获取异常")
        bad_count = "None"
    time.sleep(1)
    print("当前评论数量：" + com_all_count, com_img_count, com_video_count, com_add_count, com_good_count, com_mid_count,
          com_bad_count)
    print("好评：=====================",good_count)
    print("差评：>>>>>>>>>>>>>>>>>>>>>", bad_count)
    jd_Detail_Comment.write(f"{goods_id},{com_all_count},{com_img_count},{com_video_count},{com_add_count},{com_good_count},{com_mid_count},{com_bad_count},{good_count},{bad_count}\n")
def getCommentinfo(web, pages, type,num):
    count = ''
    current_page = 1
    # while current_page <= pages:
    if type == "good":
        counts = web.find_elements(By.XPATH, '//*[@id="comment-4"]/div/div[2]/p')
    else:
        counts = web.find_elements(By.XPATH, '//*[@id="comment-6"]/div/div[2]/p')
    for item in counts:
        web.execute_script('window.scrollTo(0, 6000)')
        count += item.text.replace("\n", ",").strip() + "|"
    if  num <=(len(count.split("|")) - 1):
        count = count.split("|")[:num]
    else:
        count = count.split("|")[:-1]
    try:
        iscom = web.execute_script(
            'return document.getElementsByClassName("ui-pager-next")[1].getAttribute("href") == "#comment"')
        if iscom:
            web.execute_script('document.getElementsByClassName("ui-pager-next")[1].click()')
            time.sleep(3)
            current_page += 1
        else:
            print("没有下一页")
            return
    except :
        print("翻页发生异常:")
        return
    time.sleep(5)  # 等待页面加载完毕

    return count


def main():
    jd_f_name = "datas/jd_getList_01.csv"

    jd_df_name = "datas/jd_getDetail_02.csv"
    jd_comment_name = "datas/jd_getComment_02.csv"
    saveDetail(jd_f_name, jd_df_name,jd_comment_name)



if __name__ == '__main__':
    main()
