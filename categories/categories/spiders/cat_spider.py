import json

from scrapy import Spider, Request

from categories.items import CatItem
from categories.settings import START_URL_TEMPLATE, CAT_URL_TEMPLATE
from categories.utils import safe_func


class OrganizationsSpider(Spider):
    name = 'cat'

    def __init__(self, region_id=None, *arg, **kwargs):
        super().__init__(*arg, **kwargs)
        self.fingerprints = set()

        # setup region_id
        if region_id is None:
            print('-' * 45)
            print('| CRITICAL: argument region_id is required! |')
            print('-' * 45)
            raise Exception('argument region_id is required!')
        self.region_id = region_id
        self.start_urls = [START_URL_TEMPLATE.format(region_id=region_id)]

    @safe_func
    def parse(self, response):
        data = json.loads(response.text)
        if data['meta']['code'] in [404, 400]:
            return
        for item in data['result']['items']:
            cat = CatItem(
                id=int(item.get('id')),
                name=item.get('name'),
                is_metarubric=item.get('type') == 'metarubric',
                region=self.region_id
            )

            if cat['is_metarubric']:
                for mod in range(-1, 2):
                    uid_mod = cat['id'] + mod
                    yield Request(url=CAT_URL_TEMPLATE.format(parent_id=uid_mod, region_id=self.region_id))

            yield cat
