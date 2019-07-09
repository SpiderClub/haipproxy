"""
This module provides basic distributed spider, inspired by scrapy-redis
"""
from scrapy import signals
from scrapy.http import Request
from scrapy.exceptions import DontCloseSpider
from scrapy.spiders import Spider
from scrapy_splash.request import SplashRequest

from haipproxy.utils import get_redis_conn
from haipproxy.config.settings import SPIDER_FEED_SIZE


class RedisSpider(Spider):
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
        self.redis_conn = get_redis_conn()
        # crawler.signals.connect(self.spider_idle, signal=signals.spider_idle)

    def next_requests(self):
        fetch_one = self.redis_conn.spop if self.use_set else self.redis_conn.lpop
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

        self.logger.info('Read {} requests from {}'.format(
            found, self.task_queue))

    def schedule_next_requests(self):
        for req in self.next_requests():
            self.crawler.engine.crawl(req, spider=self)

    def spider_idle(self):
        self.schedule_next_requests()
        raise DontCloseSpider

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        obj = super().from_crawler(crawler, *args, **kwargs)
        obj.setup_redis(crawler)
        return obj


class RedisAjaxSpider(RedisSpider):
    def next_requests(self):
        fetch_one = self.redis_conn.spop if self.use_set else self.redis_conn.lpop
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

        self.logger.info('Read {} requests from {}'.format(
            found, self.task_queue))
