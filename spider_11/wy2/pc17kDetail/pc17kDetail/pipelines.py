from .mysql import DBHelper
from .mongo import MyMongoDB


class Pc17KdetailPipeline:
    def process_item(self, item, spider):
        return item


class MysqlPipeline:
    def __init__(self):
        self.db = DBHelper("spider_db")

    def process_item(self, item, spider):
        id = item.get('id', '')
        intro = item.get('intro', '')
        auth_level = item.get('auth_level', '')
        week_click = item.get('week_click', '')
        month_click = item.get('month_click', '')
        week_up = item.get('week_up', '')
        month_up = item.get('month_up', '')
        week_tick = item.get('week_tick', '')
        month_tick = item.get('month_tick', '')
        self.db.insert(
            f"insert into book_detail(id,intro,auth_level,week_click,month_click,week_up,month_up,week_tick,month_tick)"
            f" values ('{id}','{intro}','{auth_level}','{week_click}','{month_click}','{week_up}','{month_up}'"
            f",'{week_tick}','{month_tick}')")
        print(f"当前id为{id},Mysql写入成功")
        return item


class MongodbPipeline:
    def __init__(self):
        self.db = MyMongoDB.get_db("movie")

    def process_item(self, item, spider):
        id = item.get('id', '')
        intro = item.get('intro', '')
        auth_level = item.get('auth_level', '')
        week_click = item.get('week_click', '')
        month_click = item.get('month_click', '')
        week_up = item.get('week_up', '')
        month_up = item.get('month_up', '')
        week_tick = item.get('week_tick', '')
        month_tick = item.get('month_tick', '')

        movie_dist = {"id": id, "intro": intro, "auth_level": auth_level, "week_click": week_click,
                      "month_click": month_click, "week_up": week_up, "month_up": month_up, "week_tick": week_tick,
                      "month_tick": month_tick}
        MyMongoDB.add_one(self.db, "book_detail", movie_dist)
        print(f"当前id为{id},Mongodb写入成功")
        return item
