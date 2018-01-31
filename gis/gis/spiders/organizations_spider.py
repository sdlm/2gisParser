import json
import re
import traceback

from scrapy import Spider, Request
from gis.items import OrgItem, CatItem

# noinspection SpellCheckingInspection
START_URL_TEMPLATE = 'https://catalog.api.2gis.ru/3.0/rubricator/list' \
                     '?locale=ru_RU&region_id={region_id}&key=rutnpt3272'

# noinspection SpellCheckingInspection
CAT_URL_TEMPLATE = 'https://catalog.api.2gis.ru/3.0/rubricator/list' \
                   '?parent_id={parent_id}&locale=ru_RU&region_id={region_id}&key=rutnpt3272'

# noinspection SpellCheckingInspection
ORG_URL_TEMPLATE = 'https://catalog.api.2gis.ru/2.0/catalog/branch/list' \
                   '?page={page}' \
                   '&page_size=50' \
                   '&rubric_id={rubric_id}' \
                   '&region_id={region_id}' \
                   '&locale=ru_RU' \
                   '&fields=items.contact_groups%2Citems.rubrics%2Citems.point' \
                   '&key=rutnpt3272'

page_regex = r"page=([\d]+)"
rubric_regex = r"rubric_id=([\d]+)"


def safe_func(func):

    def wrapped_func(*arg, **kwargs):
        try:
            return func(*arg, **kwargs)
        except Exception as e:
            print('- ' * 50)
            print('- ' * 50)
            print('- ' * 50)
            traceback.print_exc()
            print('- ' * 50)
            print('- ' * 50)
            print('- ' * 50)

    return wrapped_func


class OrganizationsSpider(Spider):
    name = 'organizations'

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

            else:
                yield Request(url=ORG_URL_TEMPLATE.format(rubric_id=cat['id'], region_id=self.region_id, page=1),
                              callback=self.parse_category)

            yield cat

    @safe_func
    def parse_category(self, response):
        data = json.loads(response.text)
        if data['meta']['code'] in [404, 400]:
            return

        # get next page
        url = response.request.url
        page = int(re.findall(page_regex, url)[0])
        rubric_id = int(re.findall(rubric_regex, url)[0])

        if len(data['result']['items']) > 0:
            yield Request(url=ORG_URL_TEMPLATE.format(rubric_id=rubric_id, region_id=self.region_id, page=page + 1),
                          callback=self.parse_category)

        for item in data['result']['items']:
            email = None
            if len(item.get('contact_groups', [])) == 0:
                return
            for contact in item.get('contact_groups', [{}])[0].get('contacts', []):
                if contact.get('type') == 'email':
                    email = contact.get('value')
            # skip if email does't specified
            if email is None:
                continue
            rubrics = [r.get('name') for r in item.get('rubrics', [])]
            name = item.get('name')
            address = item.get('address_name')
            fingerprint = f'{name}#{address}'
            if fingerprint not in self.fingerprints:
                self.fingerprints.add(fingerprint)
                point = item.get('point', {})
                point = point if point is not None else {}
                yield OrgItem(
                    name=name,
                    address=address,
                    lat=point.get('lat'),
                    lon=point.get('lon'),
                    email=email,
                    rubrics=json.dumps(rubrics, ensure_ascii=False),
                    region=self.region_id
                )
