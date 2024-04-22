# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import openpyxl
from openpyxl import Workbook
from .mysql import DBHelper
class MysqlPipeline:
    def __init__(self):
        self.db = DBHelper("spider_db")

    def process_item(self, item, spider):
        title = item.get('title', '')
        rating = item.get('rating', 0)
        subject = item.get('subject', '')
        duration = item.get('duration', 0)
        intro = item.get('intro', '')
        self.db.insert(f"insert into top250(title,rating,subject,duration,intro) values ('{title}','{rating}','{subject}','{duration}','{intro}')")
        return item

class ExcelPipeline:
    def __init__(self):
        self.wb = Workbook()
        self.ws = self.wb.active
        self.ws.title = "Top250"
        self.ws.append(('标题', "评分", "主题","片长","介绍"))

    def process_item(self, item, spider):
        title = item.get('title', '')
        rating = item.get('rating', '')
        subject = item.get('subject', '')
        duration = item.get('duration', 0)
        intro = item.get('intro', '')
        self.ws.append((title, rating, subject,duration,intro))
        return item

    def close_spider(self, spider):
        self.wb.save("豆瓣电影top250.xlsx")
