"""
This module provide basic distributed spider, inspired by scrapy-redis
"""
from scrapy import signals
from scrapy.http import Request
from scrapy.exceptions import DontCloseSpider
from scrapy.spiders import (
    Spider, CrawlSpider)
from scrapy_splash import SplashRequest

from utils import get_redis_conn
from config.settings import (
    VALIDATOR_FEED_SIZE, SPIDER_FEED_SIZE)

__all__ = ['RedisSpider', 'RedisAjaxSpider',
           'RedisCrawlSpider', 'ValidatorRedisSpider']


class RedisMixin(object):
    keyword_encoding = 'utf-8'
    proxy_mode = 0
    # all the redis spiders fetch task from task_type queue
    task_queue = None

    def start_requests(self):
        return self.next_requests()

    def setup_redis(self, crawler):
        """send signals when the spider is free"""
        self.redis_batch_size = SPIDER_FEED_SIZE
        self.redis_con = get_redis_conn()

        crawler.signals.connect(self.spider_idle, signal=signals.spider_idle)

    def next_requests(self):
        fetch_one = self.redis_con.lpop
        found = 0
        while found < self.redis_batch_size:
            data = fetch_one(self.task_queue)
            if not data:
                break
            url = data.decode()
            req = Request(url)
            if req:
                yield req
                found += 1

        self.logger.debug('Read {} requests from {}'.format(found, self.task_queue))

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


class RedisCrawlSpider(RedisMixin, CrawlSpider):
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
            data = fetch_one(self.task_queue)
            if not data:
                break
            url = data.decode()
            req = SplashRequest(
                url,
                args={
                    'await': 2,
                    'timeout': 90
                },
                endpoint='render.html'
            )
            if req:
                yield req
                found += 1

        self.logger.debug('Read {} requests from {}'.format(found, self.task_queue))


class ValidatorRedisSpider(RedisSpider):
    """Scrapy only supports https and http proxy"""
    def setup_redis(self, crawler):
        super().setup_redis(crawler)
        self.redis_batch_size = VALIDATOR_FEED_SIZE

    def next_requests(self):
        yield from self.next_requests_process(self.task_queue)

    def next_requests_process(self, task_type):
        fetch_one = self.redis_con.lpop
        found = 0
        while found < self.redis_batch_size:
            data = fetch_one(task_type)
            if not data:
                break
            proxy_url = data.decode()
            for url in self.urls:
                req = Request(url, meta={'proxy': proxy_url},
                              callback=self.parse, errback=self.parse_error)
                yield req
                found += 1

        self.logger.debug('Read {} ip proxies from {}'.format(found, task_type))

    def parse_error(self, failure):
        raise NotImplementedError

