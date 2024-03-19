from lxml import etree
import requests


# 爬取电影评论
def savaMovieFile():
    # f = open(fileName,mode="w",encoding='utf8')
    # f.write("id,name,info,type,pingfen,people\n")
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0",
        "Cookie": 'bid=130SUPW-zaE; ll="118204"; ap_v=0,6.0; dbcl2="258401296:YbvXkD5DPHs"; ck=FN0K; push_noty_num=0; push_doumail_num=0; frodotk_db="9d0eb15a6e22cf2bd72c140f4a686d81',
        'Referer': 'https://movie.douban.com/top250',
    }

    url = "https://movie.douban.com/subject/1292052/comments?status=P"
    html = requests.get(url,headers=headers).text
    et_html = etree.HTML(html)
    lis = et_html.xpath('//span[@class="short"]')
    for i in lis:
        comments =  i.xpath('./text()')[0].strip().replace("\n", "") +"@"
        print(comments)



    # f.close()

if __name__ == '__main__':
    fileName = "movie250.csv"
    savaMovieFile()