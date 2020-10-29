# -*- coding: utf-8 -*-
import pymongo
from pymongo.errors import DuplicateKeyError
from worker.yuqing.crawler.weibospider.settings import MONGO_HOST, MONGO_PORT

class MongoDBPipeline(object):
    def __init__(self):
        client = pymongo.MongoClient(MONGO_HOST, MONGO_PORT)
        db = client['PublicNewsComments']
        self.Users = db["Users"]
        self.Tweets = db["OriginNews"]

    def process_item(self, item, spider):
        # if spidername == 'tweet_spider':
        #     print(item)
        self.insert_item(self.Tweets, item)
        return item

    @staticmethod
    def insert_item(collection, item):
        try:
            collection.insert(dict(item))
        except DuplicateKeyError:
            pass
