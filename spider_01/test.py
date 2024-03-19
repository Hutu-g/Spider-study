import requests
url = "https://fanyi.baidu.com/v2transapi?from=en&to=zh"


param = {
"from": "en",
"to": "zh",
"query": "look",
"transtype": "realtime",
"simple_means_flag": "3",
"sign": "482316.245565",
"token": "227dc276861b7c8b9f7cc7065b0306b0",
"domain": "common",
"ts": "1709031001712"
}
haaders = {
"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
}
res =  requests.post(url,data=param , headers= haaders)
print(res.json())