# 2gis API грабер

для получения списка категорий
scrapy crawl cat --nolog -o categories.json

для получения списка организаций
scrapy crawl org --nolog -a cat=categories.json -o organizations.json
