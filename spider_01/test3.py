from urllib.request import urlopen
resp = urlopen("http://www.baidu.com") # 打开 百度
#print(resp.read().decode("utf-8")) # 打印 抓取到的内容
with open("baidu.html", mode="w", encoding="utf-8") as f: # 创建文件
    f.write(resp.read().decode("utf-8")) # 保存在⽂件中