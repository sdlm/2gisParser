import json

from scrapy import Spider, Request
from gis.items import CatItem


# noinspection SpellCheckingInspection
URL_TEMPLATE = 'https://catalog.api.2gis.ru/3.0/rubricator/list' \
               '?parent_id={parent_id}&locale=ru_RU&region_id=5&key=rutnpt3272'


class CatSpider(Spider):
    name = 'cat'
    start_urls = [
        'https://catalog.api.2gis.ru/3.0/rubricator/list?locale=ru_RU&region_id=5&key=rutnpt3272',
    ]

    def parse(self, response):
        data = json.loads(response.text)
        if data['meta']['code'] == 404:
            return
        for item in data['result']['items']:
            uid = item.get('id')
            name = item.get('name')
            if uid is not None and name is not None:
                yield CatItem(id=uid, name=name)
                yield Request(url=URL_TEMPLATE.format(parent_id=uid))
