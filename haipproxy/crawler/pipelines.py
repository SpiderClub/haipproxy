"""
scrapy pipelines for storing proxy ip infos.
"""
import logging
import time

from ..utils import get_redis_conn
from ..config.settings import (REDIS_DB, REDIS_PIPE_BATCH_SIZE)

logger = logging.getLogger(__name__)


class BasePipeline:
    def open_spider(self, spider):
        self.redis_conn = get_redis_conn()
        self.pipe = self.redis_conn.pipeline()
        self.pipe_size = 0

    def close_spider(self, spider):
        self.pipe.execute()
        logger.info(f'{self.pipe_size} redis commands executed')


class ProxyIPPipeline(BasePipeline):
    def process_item(self, item, spider):
        url = item.get('url', None)
        if not url or self.redis_conn.exists(url):
            return item
        self.pipe.hmset(
            url, {
                'used_count': 0,
                'success_count': 0,
                'total_seconds': 0,
                'last_fail': '',
                'timestamp': 0,
                'score': 0
            })
        self.pipe_size += 1
        if self.pipe_size >= REDIS_PIPE_BATCH_SIZE:
            self.pipe.execute()
            logger.info(f'{self.pipe_size} redis commands executed')
            self.pipe_size = 0
        return item


class ProxyStatPipeline(BasePipeline):
    def process_item(self, item, spider):
        self.pipe.hincrby(item['proxy'], 'used_count')
        self.pipe.hincrby(item['proxy'], 'success_count', item['success'])
        self.pipe.hincrby(item['proxy'], 'total_seconds', item['seconds'])
        self.pipe.hset(item['proxy'], 'last_fail', item['fail'])
        self.pipe.hset(item['proxy'], 'timestamp', int(time.time()))
        self.pipe.execute()
        return item
