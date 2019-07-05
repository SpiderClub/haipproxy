"""
Scrapy items for haiproxy
"""
import scrapy


class ProxyUrlItem(scrapy.Item):
    url = scrapy.Field()


class ProxyStatInc(scrapy.Item):
    proxy = scrapy.Field()
    success = scrapy.Field()
    seconds = scrapy.Field()
    fail = scrapy.Field()
