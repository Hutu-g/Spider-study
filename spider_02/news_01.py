
import requests
from bs4 import BeautifulSoup

headers = {
"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
}
f = open("news_5.csv", mode="w", encoding="utf-8")
for page in range(1,5):
    url = f"http://www.xinfadi.com.cn/newsCenter.html?current={page}"
    html = requests.get(url,headers=headers).text
    htmls = BeautifulSoup(html,"html.parser")
    divs = htmls.find_all("div",class_="col-md-10")
    for div in divs:
        title_span = div.find("p", class_="title").find_all("span")
        content_span = div.find("span",class_="content")
        title_content = [t.text for t in title_span][0]
        content_content = [t.text for t in content_span]
        a_content = div.find("a").get("href")
        f.write(f"{title_content},{content_content},{a_content}\n")
    print(f"正在下载第{page}页")
f.close()
print("采集完成")