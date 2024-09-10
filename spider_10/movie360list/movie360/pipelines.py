# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


from .mysql import DBHelper
from .mongo import MyMongoDB
class Movie360Pipeline:
    def process_item(self, item, spider):
        return item
class MysqlPipeline:
    def __init__(self):
        self.db = DBHelper("spider_db")

    def process_item(self, item, spider):
        # id = item.get('id', '')
        movie_name = item.get('movie_name', '')
        title_description = item.get('title_description', '')
        url = item.get('url', '')
        self.db.insert(
            f"insert into movie360_list(movie_name,title_description,url)"
            f" values ('{movie_name}','{title_description}','{url}')")
        print("Mysql写入成功")
        return item


class MongodbPipeline:
    def __init__(self):
        self.db = MyMongoDB.get_db("movie")

    def process_item(self, item, spider):
        movie_name = item.get('movie_name', '')
        title_description = item.get('title_description', '')
        url = item.get('url', '')
        movie_dist = {"movie_name": movie_name, "title_description": title_description, "url": url}
        MyMongoDB.add_one(self.db, "movie360_list", movie_dist)
        print("Mongodb写入成功")
        return item