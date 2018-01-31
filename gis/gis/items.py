# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CatItem(scrapy.Item):
    id = scrapy.Field(serializer=int)
    name = scrapy.Field()
    is_metarubric = scrapy.Field(serializer=bool)
    region = scrapy.Field(serializer=int)


class OrgItem(scrapy.Item):
    name = scrapy.Field()
    address = scrapy.Field()
    lat = scrapy.Field()
    lon = scrapy.Field()
    email = scrapy.Field()
    rubrics = scrapy.Field()
    region = scrapy.Field(serializer=int)
