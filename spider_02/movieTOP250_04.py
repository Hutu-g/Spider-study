import requests
import re

headers = {
"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0"
}
obj = re.compile(r'<span class="title">(?P<name>.*?)</span>.*?'
                 r'<div class="bd">.*?导演: (?P<daoyan>.*?)&nbsp;.*?主演:(?P<zhuyan>.*?)<br>(?P<time>.*?)&nbsp;.*?;(?P<contory>.*?)&nbsp;.*?;(?P<types>.*?)</p>.*?'
                 r'<span class="rating_num".*?>(?P<pingfen>.*?)</span>.*?'
                 r'<span>(?P<people>.*?)人评价</span>'
                 , re.S)
f = open("top250.csv", mode="w", encoding="utf-8")
for page in range(0,5):
    page = page * 25
    url = f"https://movie.douban.com/top250?start={page}&filter="

# url = "https://movie.douban.com/top250"
    html = requests.get(url,headers=headers).text
    res = obj.finditer(html)
    for re in res:
        name = re.group("name")
        daoyan = re.group("daoyan")
        zhuyan = re.group("zhuyan").split("...")[0]
        time = re.group("time").strip()
        pingfen = re.group("pingfen")
        people = re.group("people")
        contory = re.group("contory").strip()
        types = re.group("types").strip()
        f.write(f"{name},{daoyan},{zhuyan},{time},{contory},{types},{pingfen},{people}\n")

    print(f"第{page+1}页下载完成")
f.close()
print("数据爬完成")