import requests
import re


url = "https://movie.douban.com/top250"

headers = {
"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0"
}


resp = requests.get(url,headers=headers)
html = resp.text
obj = re.compile(r'<span class="title">(.*?)</span>.*?'
                 r'<p class="">(.*?)<br>.*?'
                r'<div class="bd">.*?<br>(.*?)&nbsp;.*?'
                r'<span class="rating_num" property="v:average">(.*?)</span>'
            ,re.S)

res = obj.findall(html)
for re in res:
    name = re[0]
    info = re[1].strip()
    time = re[2].strip()
    pingfen = re[3]
    print(name,info,time,pingfen)