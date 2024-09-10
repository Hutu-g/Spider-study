from .mysql import DBHelper
from .mongo import MyMongoDB
class Pc17KlistPipeline:
    def process_item(self, item, spider):
        return item
class MysqlPipeline:
    def __init__(self):
        self.db = DBHelper("spider_db")

    def process_item(self, item, spider):
        id = item.get('id', '')
        type = item.get('type', '')
        book_name = item.get('book_name', '')
        latest_chapter = item.get('latest_chapter', '')
        word_count = item.get('word_count', '')
        author = item.get('author', '')
        update_time = item.get('update_time', '')
        state = item.get('state', '')
        detail_url = item.get('detail_url', '')
        self.db.insert(
            f"insert into book_list(id,type,book_name,latest_chapter,word_count,author,update_time,state,detail_url)"
            f" values ('{id}','{type}','{book_name}','{latest_chapter}','{word_count}','{author}','{update_time}','{state}','{detail_url}')")
        print(f"当前id为{id},Mysql写入成功")
        return item


class MongodbPipeline:
    def __init__(self):
        self.db = MyMongoDB.get_db("movie")

    def process_item(self, item, spider):
        id = item.get('id', '')
        type = item.get('type', '')
        book_name = item.get('book_name', '')
        latest_chapter = item.get('latest_chapter', '')
        word_count = item.get('word_count', '')
        author = item.get('author', '')
        update_time = item.get('update_time', '')
        state = item.get('state', '')
        detail_url = item.get('detail_url', '')

        movie_dist = {"id": id, "type": type, "book_name": book_name, "latest_chapter": latest_chapter,
                      "word_count": word_count, "author": author, "update_time": update_time, "state": state,
                      "detail_url": detail_url}
        MyMongoDB.add_one(self.db, "book_list", movie_dist)
        print(f"当前id为{id},Mongodb写入成功")
        return item