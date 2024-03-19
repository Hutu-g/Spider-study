import fnmatch

import re
from lxml import etree
import requests
import time
def savaFile():
    # f = open(fileName,mode="w",encoding='utf8')
    # f.write("id,name,info,type,pingfen,people\n")
    headers = {
        'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Microsoft Edge";v="122"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Sec-Fetch-Site': 'same-site',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Dest': 'document',
        'Referer': 'https://account.zbj.com/login?lgtype=1&waytype=603&fromurl=https%3A%2F%2Fwww.zbj.com%2Ffw%2Fdmfj%2Fr2%2F',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'Cookie': '_uq=94c62b944a904ae647563b0301487e44; local_city_id=3467; local_city_path=quanzhou; local_city_name=%E6%B3%89%E5%B7%9E; uniqid=d014r0gi3nlnln; _suq=5d96a26a-0af4-49af-b184-29befa49bc7a; oldvid=; vid=f3eb4f6874363635c828f082b78dfa6c; unionJsonOcpc=e30=; searchTypeDataTime=1710243137182; zmId_4=%7B%22id%22%3A%22YkY5xfUz0ZSZzm0Ags5vOh2g0BOpKiBN%2BhGPom2lcD2WXXUXA67R%2FAUTpkcZslymaMIkpXcwgaiGhzqXoFrUrQ%3D%3D%22%2C%22productId%22%3A4%2C%22clickTime%22%3A1710243306699%7D; vidSended=1; nsid=s%3AvqD3SVYsQvG5XnxWirKnPUwKbSN-fizk.XVsujql0AH%2BfyX5I8jUydPwxrul98Ch0LhwAvGsDLyg; osip=1710247537272; s_s_c=xXWAc4Eno6Jb0bz4%2Fej0Dr%2F0DO4yxvdzB%2FJhiFRWl5xsOXHONxhmTsAVG9FcG8s1o0g9C%2FoQg3Bz%2BCzAt8tpFg%3D%3D; nickname=open_lz1l_uetr; brandname=open_lz1l_uetr; userid=36063367; userkey=0qxxBxXNwDCGTWnUcCz4Y%2Fwz7bh%2BnAY%2BgRIzLam0rhigQqVv7yNac1E58iK8c88Ctb%2BW6apoBoLRQB%2F3imEpQ2Z%2F%2FJZE6rvoMwkEsg%2ByNCqpztun4eB4TyrXtTcOiUYBlYqr2WcMMaEDA%2BlCg3ZAc%2BDZIdF5W0ohOph6AFY44X9CqKX5VwA4nIS4PV%2BfTGHV%2FfqHfqvgDAw7Jh8NCJNb2%2F4aVFf6sVw8V50n6TrhRe1eTd9nhqmF5uh9xZcAIP1G7B6S8Oy4lW0MbXsVjCd6TqTMIfYq%2FcJH%2ByeOpDpqDUt7l44IyLUKFNqcmzLHTOLWOFdnKxEQFQArqRyC14jye7FRl2kZ%2FQ%3D%3D'
    }

    url = "https://www.zbj.com/fw/dmfj/r2/"

    html = requests.get(url, headers=headers).text

    et_html = etree.HTML(html)
    lis = et_html.xpath('//div[@class="bot-content"]')
    for i in lis:
        title =  i.xpath('./div[2]/a/text()')[0]
        price = i.xpath('./div[1]/span/text()')[0]
        mark = i.xpath('./div[4]/div[1]/span[1]/span/text()')
        if(len(mark) == 0):
            mark = "0"
        else:
            mark = mark[0]
        sale_Num = i.xpath('./div[4]/div[2]/span/div/span[2]/text()')[0]
        good_comment_num = i.xpath('./div[4]/div[3]/span/div/span[2]/text()')[0]
        url = i.xpath('./div[2]/a/@data-href')[0]
        print(title,price,mark,sale_Num,good_comment_num,url)
    # f.close()

if __name__ == '__main__':
    savaFile()
