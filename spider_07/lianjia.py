"""
@Description：
@Author：hutu-g
@Time：2024/4/9 15:11
"""
import mongo
from mysql import DBHelper
import requests
from lxml import etree
from common.enums import URL


def getLanjia(url, cookies, pages, lianjiaFile):
    headers = {
        'sec-ch-ua': '"Microsoft Edge";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 Edg/123.0.0.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-User': '?1',
        'Sec-Fetch-Dest': 'document',
        'Referer': 'https://bj.lianjia.com/',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'Cookie': cookies
    }
    global id
    id = 0
    for page in range(1, pages + 1):
        urls = url + f"{page}"
        html = requests.get(urls, headers=headers).text
        et_html = etree.HTML(html)
        title, position, huxing, mianji, chaoxiang, zhangxiu, louceng, nianfen, jiegou = "", "", "", "", "", "", "", "", ""
        lis = et_html.xpath('//*[@id="content"]/div[1]/ul/li/div[1]')
        for li in lis:
            id += 1
            title = li.xpath('./div[1]/a/text()')[0]
            position = li.xpath("./div[2]/div/a[1]/text()")[0]
            infos = li.xpath('./div[3]/div/text()')[0].replace(" ", "").split("|")
            try:
                huxing = infos[0]
                mianji = infos[1]
                chaoxiang = infos[2]
                zhangxiu = infos[3]
                louceng = infos[4]
                if len(infos) == 7:
                    nianfen = infos[5]
                    jiegou = infos[6]
                else:
                    nianfen = "null"
                    jiegou = infos[5]
            except:
                print("youyichang")
            datas = id, title, position, huxing, mianji, chaoxiang, zhangxiu, louceng, nianfen, jiegou
            # 写入MongoDB数据库
            # safeMongo(datas)
            # 写入文件
            # lianjiaFile.write(f"{id},{title},{position},{huxing},{mianji},{chaoxiang},{zhangxiu},{louceng},{nianfen},{jiegou}\n")
            # 写入Mysql数据库
            # safeMysql(datas)
            # 打印
            print(datas)

def safeMongo(data):
    id, title, position, huxing, mianji, chaoxiang, zhangxiu, louceng, nianfen, jiegou = data
    db = mongo.get_db("lianjia")
    house_dist = {"id": id, "title": title, "position": position, "huxing": huxing, "mianji": mianji,
                  "chaoxiang": chaoxiang, "nianfen": nianfen, "zhangxiu": zhangxiu, "louceng": louceng,
                  "jiegou": jiegou}
    mongo.add_one(db, "house", house_dist)
    print("写入成功")


def safeMysql(data):
    id, title, position, huxing, mianji, chaoxiang, zhangxiu, louceng, nianfen, jiegou = data
    with DBHelper("spider_db") as db:
        db.insert(
            f"insert into lianjia(id,title, position, huxing, mianji, chaoxiang, zhangxiu, louceng, nianfen, jiegou) values ('{id}','{title}','{position}','{huxing}','{mianji}','{chaoxiang}','{zhangxiu}','{louceng}','{nianfen}','{jiegou}')")

    print("写入成功")

def main():
    url = URL.lianjia['url']
    cookies = URL.lianjia['cookies']
    pages = 2
    lianjiaFile = open("lianjie.csv", mode="a", encoding='utf8')
    getLanjia(url, cookies, pages, lianjiaFile)
    lianjiaFile.close()


if __name__ == '__main__':
    main()
