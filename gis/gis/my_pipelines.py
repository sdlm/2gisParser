# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
from scrapy.exceptions import DropItem


class GisPipeline(object):
    def process_item(self, item, spider):
        del spider
        return item


# noinspection PyUnusedLocal
class MongoPipeline(object):

    collection_name = 'scrapy_items'

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE', 'items')
        )

    # noinspection PyAttributeOutsideInit
    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        self.db[self.collection_name].insert_one(dict(item))
        return item


class DuplicatesPipeline(object):

    def __init__(self):
        self.fingerprints = set()

    def process_item(self, item, spider):
        del spider
        name = item.get('name')
        address = item.get('address_name')
        fingerprint = f'{name}#{address}'
        if fingerprint in self.fingerprints:
            raise DropItem("Duplicate item found: %s" % item)
        else:
            self.fingerprints.add(fingerprint)
            return item
