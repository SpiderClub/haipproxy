"""
Scrapy items for haiproxy
"""
import scrapy


class ProxyIPItem(scrapy.Item):
    ip = scrapy.Field()
    port = scrapy.Field()
    # 0 stands for http,1 stands for https, 2 stands for socks4/5
    protocol = scrapy.Field()


class ProxyUrlItem(scrapy.Item):
    url = scrapy.Field()


