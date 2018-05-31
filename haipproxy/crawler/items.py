"""
Scrapy items for haiproxy
"""
import scrapy


class ProxyUrlItem(scrapy.Item):
    url = scrapy.Field()


class ProxyScoreItem(scrapy.Item):
    url = scrapy.Field()
    score = scrapy.Field()
    incr = scrapy.Field()
    queue = scrapy.Field()


class ProxyVerifiedTimeItem(scrapy.Item):
    url = scrapy.Field()
    verified_time = scrapy.Field()
    incr = scrapy.Field()
    queue = scrapy.Field()


class ProxySpeedItem(scrapy.Item):
    url = scrapy.Field()
    response_time = scrapy.Field()
    incr = scrapy.Field()
    queue = scrapy.Field()