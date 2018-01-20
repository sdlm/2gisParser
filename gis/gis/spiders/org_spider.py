import json

from scrapy import Spider, Request
from gis.items import CatItem, OrgItem

# noinspection SpellCheckingInspection
URL_TEMPLATE = 'https://catalog.api.2gis.ru/2.0/catalog/branch/list' \
               '?page=1' \
               '&page_size=50' \
               '&rubric_id={rubric_id}' \
               '&region_id=5' \
               '&locale=ru_RU' \
               '&fields=items.contact_groups%2Citems.point' \
               '&key=rutnpt3272'


class OrgSpider(Spider):
    name = 'org'

    def start_requests(self):
        cat_file = getattr(self, 'cat', None)
        if cat_file is None:
            return
        with open(cat_file) as categories:
            for item in json.loads(categories.read()):
                yield Request(URL_TEMPLATE.format(rubric_id=item['id']), self.parse)

    def parse(self, response):
        data = json.loads(response.text)
        if data['meta']['code'] == 404:
            return
        for item in data['result']['items']:
            emails = list()
            for contact in item.get('contact_groups', [{}])[0].get('contacts', []):
                if contact.get('type') == 'email':
                    emails.append(contact.get('value'))
            if emails:
                yield OrgItem(
                    name=item.get('name'),
                    address=item.get('address_name'),
                    lat=item.get('point', {}).get('lat'),
                    lon=item.get('point', {}).get('lon'),
                    email=emails[0] if len(emails) > 0 else None,
                    email2=emails[1] if len(emails) > 1 else None,
                    email3=emails[2] if len(emails) > 2 else None,
                )
