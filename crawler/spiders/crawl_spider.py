"""
Crawlspider for haipproxy.

"""
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor

from config.settings import SPIDER_CRAWL_TASK
from ..redis_spiders import RedisCrawlSpider
from .mixin import BaseSpider


class CrawlSpider(BaseSpider, RedisCrawlSpider):
    name = 'crawl'
    task_type = SPIDER_CRAWL_TASK
    # todo register allowed_domains and rules dynamicly
    # todo find out why sometimes or in what page we get port of empty value
    allowed_domains = ['coderbusy.com']
    rules = (
        Rule(LinkExtractor(allow=(r'/classical/',), deny=(r'fetch.aspx', r'transparent.aspx',)),
             callback='parse_proxy_info', follow=True),
    )

    def parse_proxy_info(self, response):
        items = self.parse_common(response)
        for item in items:
            yield item





