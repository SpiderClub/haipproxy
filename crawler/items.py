"""
Scrapy items for haiproxy
"""
import scrapy


class ProxyUrlItem(scrapy.Item):
    url = scrapy.Field()


class ProxyDetailItem(scrapy.Item):
    url = scrapy.Field()
    score = scrapy.Field()
    queue = scrapy.Field()