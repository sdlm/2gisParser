import json

import scrapy


class DashboardSpider(scrapy.Spider):
    name = 'dashboard'
    start_urls = ['https://catalog.api.2gis.ru/3.0/rubricator/dashboard?locale=ru_RU&region_id=5&key=rutnpt3272']

    def parse(self, response):
        data = json.loads(response.text)
        items = [i.get('search_query') for i in data['result']['items'] if i.get('search_query')]
        return {num: item for num, item in enumerate(items)}
