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
        type = item.get('type', '')
        year = item.get('year', '')
        area = item.get('area', '')
        director = item.get('director', '')
        peoples = item.get('peoples', '')
        movie_description = item.get('movie_description', '')
        vod_name = item.get('vod_name', '')

        self.db.insert(
            f"insert into movie360(movie_name,title_description,url,type,year,area,director,peoples,movie_description,vod_name)"
            f" values ('{movie_name}','{title_description}','{url}','{type}','{year}','{area}','{director}','{peoples}','{movie_description}','{vod_name}')")
        print("Mysql写入成功")
        return item


class MongodbPipeline:
    def __init__(self):
        self.db = MyMongoDB.get_db("movie")

    def process_item(self, item, spider):
        movie_name = item.get('movie_name', '')
        title_description = item.get('title_description', '')
        url = item.get('url', '')
        type = item.get('type', '')
        year = item.get('year', '')
        area = item.get('area', '')
        director = item.get('director', '')
        peoples = item.get('peoples', '')
        movie_description = item.get('movie_description', '')
        vod_name = item.get('vod_name', '')

        movie_dist = {"movie_name": movie_name, "title_description": title_description, "url": url, "type": type,
                      "year": year, "area": area, "director": director, "peoples": peoples,
                      "movie_description": movie_description, "vod_name": vod_name}
        MyMongoDB.add_one(self.db, "movie360", movie_dist)
        print("Mongodb写入成功")
        return item