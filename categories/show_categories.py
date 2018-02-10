#!/usr/bin/env python

import pymongo

if __name__ == '__main__':
    client = pymongo.MongoClient("localhost", 27017)
    db = client.gis_db
    for item in db.scrapy_items.find():
        print(item)
