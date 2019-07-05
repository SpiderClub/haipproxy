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
        self.rpipe = self.redis_conn.pipeline()
        self.rpipe_size = 0

    def close_spider(self, spider):
        self.rpipe.execute()
        logger.info(f'{self.rpipe_size} redis commands executed')


class ProxyIPPipeline(BasePipeline):
    def process_item(self, item, spider):
        url = item.get('url', None)
        if not url or self.redis_conn.exists(url):
            return item
        self.rpipe.hmset(
            url, {
                'used_count': 0,
                'success_count': 0,
                'total_seconds': 0,
                'last_fail': '',
                'timestamp': 0,
                'score': 0
            })
        self.rpipe_size += 1
        if self.rpipe_size >= REDIS_PIPE_BATCH_SIZE:
            self.rpipe.execute()
            logger.info(f'{self.rpipe_size} redis commands executed')
            self.rpipe_size = 0
        return item


class ProxyStatPipeline(BasePipeline):
    def process_item(self, item, spider):
        self.rpipe.hincrby(item['proxy'], 'used_count')
        self.rpipe.hincrby(item['proxy'], 'success_count', item['success'])
        self.rpipe.hincrby(item['proxy'], 'total_seconds', item['seconds'])
        self.rpipe.hset(item['proxy'], 'last_fail', item['fail'])
        self.rpipe.hset(item['proxy'], 'timestamp', int(time.time()))
        self.rpipe.execute()
        return item
