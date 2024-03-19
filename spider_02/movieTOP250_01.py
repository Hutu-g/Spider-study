import requests
import re


url = "https://movie.douban.com/top250"

param = {
"type": "13",
"interval_id": "100:90",
"action": "",
"start": "0",
"limit": "20"
}

headers = {
"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0"
}


resp = requests.get(url,headers=headers)
html = resp.text
movie_ol = re.findall(r'<ol class="grid_view">(.*?)</ol>',html,re.S)[0]

movie_lis = re.findall(r'<li>(.*?)</li>',movie_ol,re.S)

for li in movie_lis:
    name = re.findall(r'<span class="title">(.*?)</span>',li,re.S)[0]
    des = re.findall(r'<div class="bd">.*?<br>(.*?)&nbsp;', li, re.S)[0].strip()
    pingfen = re.findall(r'<span class="rating_num" property="v:average">(.*?)</span>', li, re.S)[0]
    info = re.findall(r'<div class="bd">.*?导演：(.*?)&nbsp;.*?<br>', li, re.S)
    print(name,des,pingfen,info)
