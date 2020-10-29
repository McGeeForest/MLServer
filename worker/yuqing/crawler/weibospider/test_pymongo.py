# -*- coding: utf-8 -*-
"""
Created on Wed Aug 26 14:52:26 2020

@author: lh
"""
import pymongo 

"""
client = pymongo.MongoClient(host='localhost', port=27017) 
db = client['weibo']
collection = db['Tweets_2020-07_\u5316\u5DE5\u4E8B\u6545']
results = collection.find({"comment_num":{"$gt":0}})
tweets_ids = []
for result in results:
    tweets_ids.append(result['_id'])
"""

client = pymongo.MongoClient(host='localhost', port=27017) 
db = client['weibo']
collection = db['Comments']
results = collection.find({"like_num":{"$gt":0}})
comments = {}
for comment in results:
    comments.update({comment['content']:comment['like_num']})
print(comments)    
        