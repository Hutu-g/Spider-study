import fnmatch

import re
from lxml import etree
import requests
import time
def getListMoviePage(f,end):
    global id
    id = 0
    global headers
    headers= {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0",
        "Cookie":'bid=130SUPW-zaE; ll="118204"; ap_v=0,6.0; dbcl2="258401296:YbvXkD5DPHs"; ck=FN0K; push_noty_num=0; push_doumail_num=0; frodotk_db="9d0eb15a6e22cf2bd72c140f4a686d81',
        'Referer': 'https://movie.douban.com/top250',
    }
    for i in range(end):
        url = f"https://movie.douban.com/top250?start={ i * 25}"
        html = requests.get(url,headers=headers).text
        parseMovie(f,html)
    print("正在获取数据")
id = 0
def parseMovie(f,html):
    et_html = etree.HTML(html)
    lis = et_html.xpath('//*[@id="content"]/div/div[1]/ol/li')
    global id
    for li in lis:

        id =id+1
        name = li.xpath("./div/div[2]/div[1]/a/span[1]/text()")[0].replace(" ", "")
        url = li.xpath("./div/div[1]/a/@href")[0].strip()
        url_html = requests.get(url,headers=headers).text
        et_url_html = etree.HTML(url_html)

        bianju =  et_url_html.xpath('//*[@id="info"]/span[2]/span[2]/a/text()')
        bianju = ";".join(bianju)

        languages = et_url_html.xpath('//*[@id="info"]/text()')
        language = fnmatch.filter(languages,'*语*')[0].strip()
        if (len(language) == 0):
            language = ''

        times1 = et_url_html.xpath('//*[@id="info"]/span')[-3].xpath('./text()')
        times2 = et_url_html.xpath('//*[@id="info"]/span')[-4].xpath('./text()')
        times1 = fnmatch.filter(times1,'*分钟*')
        times2 = fnmatch.filter(times2, '*分钟*')
        '//*[@id="review_1000369_short"]/div/text()[1]'
        if (len(times1) != 0):
            times = re.findall('\d+', times1[0])[0]
        elif(len(times2) != 0):
            times = re.findall('\d+', times2[0])[0]
        else:
            times = ''

        data = et_url_html.xpath('//*[@id="link-report-intra"]/span/text()')
        datas = [i.strip() for i in data]
        data = "".join(datas).strip()
        print()
        f.write(f"{id},{name},{bianju},{language},{times},{data},{url}\n")
        print(id,name,bianju,language,times,data,url)
        time.sleep(1)
    print("解析完毕")
    '//*[@id="info"]'
def saveMovieFile(fileName,end):
    f = open(fileName,mode="w",encoding='utf8')
    f.write("id,name,bianju,language,times,data,url\n")
    getListMoviePage(f,end)
    f.close()
    print("下载完成")

if __name__ == '__main__':
    fileName = "movie250_url_data_03.csv"
    endPage = 3
    saveMovieFile(fileName,endPage)