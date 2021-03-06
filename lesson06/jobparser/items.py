# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class JobparserItem(scrapy.Item):
    # define the fields for your item here like:
    _id = scrapy.Field()
    name = scrapy.Field()
    salary = scrapy.Field()
    salary_min = scrapy.Field()
    salary_max = scrapy.Field()
    salary_currency = scrapy.Field()
    company_name = scrapy.Field()
    company_address = scrapy.Field()
    site = scrapy.Field()

    link = scrapy.Field()