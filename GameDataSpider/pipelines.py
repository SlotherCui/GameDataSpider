# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

mongo_host = 'localhost'
mongo_port = 27017
mongo_db_name = 'spider'
mongo_db_collection = 'Tdm_game_data_desc'
import pymongo
class ScrapyseleniumtestPipeline(object):

    def __init__(self):
        client = pymongo.MongoClient(host=mongo_host, port = mongo_port)
        db  = client[mongo_db_name]
        self.post = db[mongo_db_collection]


    def process_item(self, item, spider):
        if spider.name == 'TreeDM':
            # print('here')
            self.post.update({"game_link":item['game_link']},{"$set":{"game_img":item['game_img']}})
            return item
        # data = dict(item)
        # print(data)
        # self.post.insert(data)
        # return item
