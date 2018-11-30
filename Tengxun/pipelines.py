# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from . import settings
import pymongo


class TengxunPrintPipeline(object):
	def process_item(self, item, spider):
		print(item)
		print("-------")
		return item


class TengxunMongoPipeline(object):

	def __init__(self):
		host = settings.MONGODB_HOST
		port = settings.MONGODB_PORT
		dbname = settings.MONGODB_DATABASE
		tname = settings.MONGODB_TABLE
		# 创建连接对象
		conn = pymongo.MongoClient(host=host, port=port)
		# 创建库对象
		db = conn[dbname]
		# 集合对象　
		self.myset = db[tname]
		

	def process_item(self, item, spider):
		infoDict = dict(item)
		self.myset.insert(infoDict)
		print("保存成功")
		return item
