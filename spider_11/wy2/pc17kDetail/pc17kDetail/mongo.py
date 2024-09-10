
import pymongo

class MyMongoDB:
    def get_db(database):
        conn = pymongo.MongoClient(host='localhost', port=27017)
    # 切换数据库
        db = conn[database]
        return db
    def add_one(db, table, data):
        result = db[table].insert_one(data)
        return result
    def add_many(db, table, data_list):
        result = db[table].insert_many(data_list)
        return result
    def upd(db, table, condition, data):
        result = db[table].update_many(condition, {'$set':data})
        return result
    def delete(db, table, condition):
        result = db[table].delete_many(condition)
        return result
    def query(db, table, condition=''):
        result = db[table].find(condition)
        return result