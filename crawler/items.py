"""
Scrapy items for haiproxy
"""
import scrapy


class ProxyUrlItem(scrapy.Item):
    url = scrapy.Field()


