"""
This module provide basic distributed spider, inspired by scrapy-redis
"""
from scrapy import signals
from scrapy.http import Request
from scrapy.exceptions import DontCloseSpider
from scrapy.spiders import Spider
from scrapy_splash import SplashRequest

from utils.connetion import get_redis_con


__all__ = ['RedisSpider', 'RedisAjaxSpider']


class RedisMixin(object):
    keyword_encoding = 'utf-8'
    proxy_mode = 0

    def start_requests(self):
        return self.next_requests()

    def setup_redis(self, crawler):
        """send signals when the spider is free"""
        settings = crawler.settings
        self.redis_batch_size = settings.getint('SPIDER_FEED_SIZE')
        self.redis_con = get_redis_con()

        crawler.signals.connect(self.spider_idle, signal=signals.spider_idle)

    def next_requests(self):
        fetch_one = self.redis_con.lpop
        found = 0
        while found < self.redis_batch_size:
            data = fetch_one(self.task_type)
            if not data:
                break
            url = data.decode()
            req = Request(url)
            if req:
                yield req
                found += 1

        self.logger.debug('Read {} requests from {}'.format(found, self.task_type))

    def schedule_next_requests(self):
        for req in self.next_requests():
            self.crawler.engine.crawl(req, spider=self)

    def spider_idle(self):
        self.schedule_next_requests()
        raise DontCloseSpider


class RedisSpider(RedisMixin, Spider):
    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        obj = super().from_crawler(crawler, *args, **kwargs)
        obj.setup_redis(crawler)
        return obj


class RedisAjaxSpider(RedisSpider):
    def next_requests(self):
        fetch_one = self.redis_con.lpop
        found = 0
        while found < self.redis_batch_size:
            data = fetch_one(self.task_type)
            if not data:
                break
            url = data.decode()
            req = SplashRequest(url, args={'await': 0.25})
            if req:
                yield req
                found += 1

        self.logger.debug('Read {} requests from {}'.format(found, self.task_type))


