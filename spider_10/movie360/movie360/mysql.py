import pymysql
from pymysql.cursors import DictCursor
"""
@Description：
@Author：hutu-g
@Time：2024/4/9 17:01
"""
class DBHelper:
    def __init__(self, database=None, host="localhost", port=3306,username="root", password="123456"):
        self.conn = pymysql.connect(
        host=host,
        port=port,
        user=username,
        password=password,
        database=database)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        return self.conn.close()

    def _change(self, sql, *args, isInsert=False):
        cursor = self.conn.cursor()
        try:
            rownum = cursor.execute(sql, args)
            self.conn.commit()
            if isInsert:
                return cursor.lastrowid
            else:
                return rownum
        except Exception as e:
            print("报错了", e)
            self.conn.rollback()
        finally:
            cursor.close()

    def insert(self, sql, *args):
        return self._change(sql, *args, isInsert=True)

    def update(self, sql, *args):
        return self._change(sql, *args)

    def delete(self, sql, *args):
        return self._change(sql, *args)
    def query_list(self, sql, *args):
        cursor = self.conn.cursor(DictCursor)
        try:
            cursor.execute(sql, args)
            result = cursor.fetchall()
            return result
        finally:
            cursor.close()

    def query_one(self, sql, *args):
        cursor = self.conn.cursor(DictCursor)
        try:
            cursor.execute(sql, args)
            result = cursor.fetchone()
            return result
        finally:
            cursor.close()


