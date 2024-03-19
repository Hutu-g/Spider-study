import requests
url = "https://movie.douban.com/j/chart/top_list"

param = {
"type": "13",
"interval_id": "100:90",
"action": "",
"start": "0",
"limit": "20"
}

headers = {
"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
}
res = requests.get(url, params=param,headers=headers).json()
# print(res[0])
for i in res:
    print(i)

