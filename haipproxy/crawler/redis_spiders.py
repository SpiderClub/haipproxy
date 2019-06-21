"""
This module provides basic distributed spider, inspired by scrapy-redis
"""
import logging

from scrapy import signals
from scrapy.http import Request
from scrapy.exceptions import DontCloseSpider
from scrapy.spiders import (Spider, CrawlSpider)
from scrapy_splash.request import SplashRequest
# from scrapy.utils.log import configure_logging

from ..utils import get_redis_conn
from ..config.settings import (VALIDATOR_FEED_SIZE, SPIDER_FEED_SIZE)

# configure_logging(install_root_handler=True)
__all__ = [
    'RedisSpider', 'RedisAjaxSpider', 'RedisCrawlSpider',
    'ValidatorRedisSpider'
]

logger = logging.getLogger(__name__)

class RedisMixin(object):
    keyword_encoding = 'utf-8'
    proxy_mode = 0
    # if use_set=True, spider fetches data from set other than list
    use_set = False
    # all the redis spiders fetch task from task_queue queue
    task_queue = None

    def start_requests(self):
        return self.next_requests()

    def setup_redis(self, crawler):
        """send signals when the spider is free"""
        self.redis_batch_size = SPIDER_FEED_SIZE
        self.redis_con = get_redis_conn()

        crawler.signals.connect(self.spider_idle, signal=signals.spider_idle)

    def next_requests(self):
        fetch_one = self.redis_con.spop if self.use_set else self.redis_con.lpop
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

        logger.info('Read {} requests from {}'.format(found, self.task_queue))

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
        fetch_one = self.redis_con.spop if self.use_set else self.redis_con.lpop
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
            )
            if req:
                yield req
                found += 1

        logger.info('Read {} requests from {}'.format(found, self.task_queue))


class ValidatorRedisSpider(RedisSpider):
    """Scrapy only supports https and http proxy"""

    def setup_redis(self, crawler):
        super().setup_redis(crawler)
        self.redis_batch_size = VALIDATOR_FEED_SIZE

    def next_requests(self):
        yield from self.next_requests_process(self.task_queue)

    def next_requests_process(self, task_queue):
        fetch_one = self.redis_con.spop if self.use_set else self.redis_con.lpop
        found = 0
        while found < self.redis_batch_size:
            data = fetch_one(task_queue)
            if not data:
                break
            proxy_url = data.decode()
            for url in self.urls:
                req = Request(url,
                              meta={'proxy': proxy_url},
                              callback=self.parse,
                              errback=self.parse_error)
                yield req
                found += 1
        logger.info('Read {} ip proxies from {}'.format(found, task_queue))

    def parse_error(self, failure):
        raise NotImplementedError
