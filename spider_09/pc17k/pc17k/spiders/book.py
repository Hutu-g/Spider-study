import scrapy
from scrapy.http import HtmlResponse


class BookSpider(scrapy.Spider):
    name = "book"
    allowed_domains = ["www.17k.com"]


    def start_requests(self):
        url = 'https://user.17k.com/ck/author2/shelf?page=1&appKey=2406394919'
        cookie_dic = {}
        cookies = "GUID=db79cd9d-24f6-4b4f-bd60-4b0479d291a0; acw_sc__v2=6631c7f4ff3327019bfdfccff36a9d2207b6c84d; sajssdk_2015_cross_new_user=1; Hm_lvt_9793f42b498361373512340937deb2a0=1714538484; accessToken=avatarUrl%3Dhttps%253A%252F%252Fcdn.static.17k.com%252Fuser%252Favatar%252F09%252F69%252F93%252F103289369.jpg-88x88%253Fv%253D1710844416000%26id%3D103289369%26nickname%3Dbfhjkbwhbf%26e%3D1730090499%26s%3Dada368d407df6678; c_channel=0; c_csc=web; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22103289369%22%2C%22%24device_id%22%3A%2218f3275115ea88-049eb995f5477a-26001d51-2073600-18f3275115f1988%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%2C%22first_id%22%3A%22db79cd9d-24f6-4b4f-bd60-4b0479d291a0%22%7D; ssxmod_itna=YuiQPfxAxUxx7zDXWPOhaWY0QDCWDRomgOi4mg4GXeoDZDiqAPGhDCb8F2k80e+5KLG0gbAs6znLPR5L4aYnfv/mDB3DEx0=tv3D0KoD4SKGwD0eG+DD4DWUx03DoxGAgwx04kg92u9QD3qDwDB=DmqG24m=Dm4DfDDd9WBx0zG=nDYQDGqDS3mTDxD3DfS65DDXY+7DNKMxDbh6SRS0DTnTtfMD9D0tDIqGXii7QgCB+s7XS9ZG7H2j4deGuDG=KvkLex0pySMU2+a+xW7pRp05NmDhFBADN4EbtDTxWzihNB0dd42mrYh7j0eKBA30qjGDPD==; ssxmod_itna2=YuiQPfxAxUxx7zDXWPOhaWY0QDCWDRomgOi4mxA=c+YD/lBDjx7PAS4Xhg+yw8Nf=MPwGqVoWYrH5OfeE5vovK8fnp2I8dLrhQzhYy60TaCeQvEfdGC0nyOOMzQ2BYky9tlE4cV4GF8TYeiY0xr40MY4icR4i2zn2ewQ2uzjbKg+REGCQ0DnIy7eLe=8nD6gNDp8aaTlaKXmToLd0opP6DHCywQW28eQrzP/LHeb7+i/NegGqsinieTB51rWxOzgUnFk32/uA9DMaqq5Xyi6c8DLGy7K3IimYLRfEj3pYld8dX=uVSq9s0aceRDiDMt+4n9ViRjYROb94pwV+A8fAUBPXm5x5+3D0780qMG3PGqNi=sYN7kmDEmvjKEjKhBxW2qY0KuDpQG5VA=9evfOImlx+7YhkDND8ghAFOKKhxQDDLxD2zGDD===; tfstk=fdRprO2BJcmhaGkkOeMM4OTD_P3iSBLF-H8bZgj3FhK9lErhF9NI2dKWb9jBwUPRPUtr8g0EIe8Fa_imm_hD8e5nLQyW99T15wY_Fk_GNOJPa_imjRV5LjCymwt4pDLsWablV8t5dlT1baF7d3sCCl_Au_sWV_gOCZb4Ry_CRO118vIs2GaCq7dM7C9mW-cbw7dO50SXJkNcJCbdpiTB9SVm5wBdcestmxl36OTPeQzzwMTB337XAkicLU99XwC-sJ1XWLtA7BG0vNJH5Ej6krNX86pvM69KbR5HvC16OKU7NFCdYO_dBknOcB86g16iGqL6_HYe6U4SNNxcfeRCwjgV96sC6NRobWsJCLOhL_rIm98WBhQdGg72iIHnLojArJgtW8yPdNbBg3SeK8mayNImSR2zUObNWi09x8yPQQ_OmVcbU8WGW; Hm_lpvt_9793f42b498361373512340937deb2a0=1714538527"
        for c in cookies.split("; "):
            kv = c.split("=")
            k = kv[0]
            v = "".join(kv[1:])
            cookie_dic[k] = v
        yield scrapy.Request(url=url, cookies=cookie_dic, callback=self.parse)

    def parse(self, response:HtmlResponse,**kwargs):
        print(response.json())
        pass
