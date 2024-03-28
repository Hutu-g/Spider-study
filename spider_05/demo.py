# -- coding:utf-8 --
"""
@Description：
@Author：hutu-g
@Time：2024/3/27 14:01
"""

from urllib.parse import urlparse, urlunparse, urlencode, quote_plus


'https://search.jd.com/Search?keyword=%E6%99%BA%E8%83%BD%E6%89%8B%E6%9C%BA&enc=utf-8&wq=%E6%99%BA%E8%83%BD%E6%89%8B%E6%9C%BA&pvid=7c6c8aef086f4f94988dadfa6df39c16'

def encode_url(url):
    # 解析URL
    parsed_url = urlparse(url)
    # 解析查询参数，转换成字典
    query_params = dict(qc.split('=') for qc in parsed_url.query.split('&'))

    # 对查询参数中的键和值进行编码
    encoded_query_params = {quote_plus(k): quote_plus(v) for k, v in query_params.items()}

    # 使用urlencode方法将查询参数编码成字符串
    encoded_query_string = urlencode(encoded_query_params, safe="=&")

    # 重新构建URL
    encoded_url = urlunparse((
        parsed_url.scheme,  # 协议，如 "http"
        parsed_url.netloc,  # 网络位置，如 "search.jd.com"
        parsed_url.path,  # 路径，如 "/Search"
        parsed_url.params,  # 参数，通常为空
        encoded_query_string,  # 编码后的查询字符串
        parsed_url.fragment  # 锚点，通常为空
    ))

    return encoded_url


# 原始URL
original_url = "https://search.jd.com/Search?keyword=智能手机&qrst=1&wq=智能手机&stock=1&pvid=7c6c8aef086f4f94988dadfa6df39c16&isList=0&page=1"

# 编码后的URL
encoded_url = encode_url(original_url)

print("编码后的URL:", encoded_url)
