# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from .mysql import DBHelper
from .mongo import MyMongoDB


class LianjiaPipeline:
    def process_item(self, item, spider):
        return item


class MysqlPipeline:
    def __init__(self):
        self.db = DBHelper("spider_db")

    def process_item(self, item, spider):
        # id = item.get('id', '')
        title = item.get('title', 0)
        position = item.get('position', '')
        huxing = item.get('huxing', 0)
        mianji = item.get('mianji', '')
        chaoxiang = item.get('chaoxiang', '')
        zhangxiu = item.get('zhangxiu', 0)
        louceng = item.get('louceng', '')
        nianfen = item.get('nianfen', 0)
        jiegou = item.get('jiegou', '')
        self.db.insert(
            f"insert into lianjia_scrapy(title,position,huxing,mianji,chaoxiang,zhangxiu,louceng,nianfen,jiegou) values ('{title}','{position}','{huxing}','{mianji}','{chaoxiang}','{zhangxiu}','{louceng}','{nianfen}','{jiegou}')")
        return item


class MongodbPipeline:
    def __init__(self):
        self.db = MyMongoDB.get_db("lianjia")

    def process_item(self, item, spider):
        title = item.get('title', 0)
        position = item.get('position', '')
        huxing = item.get('huxing', 0)
        mianji = item.get('mianji', '')
        chaoxiang = item.get('chaoxiang', '')
        zhangxiu = item.get('zhangxiu', 0)
        louceng = item.get('louceng', '')
        nianfen = item.get('nianfen', 0)
        jiegou = item.get('jiegou', '')

        house_dist = {"title": title, "position": position, "huxing": huxing, "mianji": mianji,
                      "chaoxiang": chaoxiang, "nianfen": nianfen, "zhangxiu": zhangxiu, "louceng": louceng,
                      "jiegou": jiegou}
        MyMongoDB.add_one(self.db, "lianjia_scrapu", house_dist)
        print("写入成功")
        return item
