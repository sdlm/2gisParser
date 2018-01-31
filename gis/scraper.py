#!/usr/bin/env python

import json
import traceback
from optparse import OptionParser

from scrapy.crawler import CrawlerProcess

from gis.spiders.organizations_spider import OrganizationsSpider

if __name__ == '__main__':

    parser = OptionParser()
    parser.add_option('-r', '--region', dest='region', help='scraping data for region', metavar='INT')

    (options, args) = parser.parse_args()

    try:
        # getter
        assert options.region
        regions = json.loads(f'[{options.region}]')

        # validation
        assert isinstance(regions, list)
        for i in regions:
            assert isinstance(i, int)

    except Exception:
        traceback.print_exc()
        print('''Usage: scraper.py [options]
Options:
  -h, --help            show this help message and exit
  -r INT, --region=INT  scraping data for region
''')

    else:
        config = {
            'FEED_URI': f'results.json',
            'FEED_FORMAT': 'json',
            'FEED_EXPORT_ENCODING': 'utf-8',
            'ROBOTSTXT_OBEY': False,
        }
        process = CrawlerProcess(config)
        for i in regions:
            process.crawl(OrganizationsSpider, region_id=i)
        process.start()
