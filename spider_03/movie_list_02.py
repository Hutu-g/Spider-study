from lxml import etree
import requests
def getListMoviePage(f,end):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0",
        "Cookie": 'bid=130SUPW-zaE; ll="118204"; ap_v=0,6.0; dbcl2="258401296:YbvXkD5DPHs"; ck=FN0K; push_noty_num=0; push_doumail_num=0; frodotk_db="9d0eb15a6e22cf2bd72c140f4a686d81',
        'Referer': 'https://movie.douban.com/top250',
    }
    for i in range(end):
        url = f"https://movie.douban.com/top250?start={ i * 25}"
        html = requests.get(url,headers=headers).text
        parseMovie(f,html)
    print("正在获取数据")

id = 0
def parseMovie(f,html):
    global id
    et_html = etree.HTML(html)
    lis = et_html.xpath('//*[@id="content"]/div/div[1]/ol/li')
    for li in lis:
        id =id+1
        name = li.xpath("./div/div[2]/div[1]/a/span[1]/text()")[0].replace(" ", "")
        info = li.xpath("./div/div[2]/div[2]/p[1]/text()")[0].strip().replace(" ", "")
        type = li.xpath("./div/div[2]/div[2]/p[1]/text()[2]")[0].strip().replace(" ", "")
        pingfen = li.xpath("./div/div[2]/div[2]/div/span[2]/text()")[0].strip().replace(" ", "")
        people = li.xpath("./div/div[2]/div[2]/div/span[4]/text()")[0][:-3].strip().replace(" ", "")
        url = li.xpath("./div/div[1]/a/@href")[0].strip()
        f.write(f"{id},{name},{info},{type},{pingfen},{people},{url}\n")
        print(name,info,type,pingfen,people,url)
    print("解析完毕")
def saveMovieFile(fileName,end):
    f = open(fileName,mode="w",encoding='utf8')
    f.write("id,name,info,type,pingfen,people\n")
    getListMoviePage(f,end)
    f.close()
    print("下载完成")



if __name__ == '__main__':
    fileName = "movie250_02.csv"
    endPage = 3
    saveMovieFile(fileName,endPage)