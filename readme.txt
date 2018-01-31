# 2gis API грабер

для получения списка организаций
> scrapy crawl organizations --nolog -a region_id=5 -o result_of_region_5.json

для конвертации в Excel
> json_to_xlsx.py result_of_region_5.json

что бы последовательно сграбить несколько регионов (в рамках одного процесса)
> scraper.py -r 4,5,6,7

region_id:
1 - Новосибирск
2 - Омск
3 - Томск
4 - Барнаул
5 - Кемерово
6 - Новокузнецк
7 - Красноярск
