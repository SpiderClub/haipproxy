"""
scrapy pipelines for storing proxy ip infos.
"""
from twisted.internet.threads import deferToThread
from scrapy.exceptions import DropItem

from ..utils import get_redis_conn
from ..config.settings import (REDIS_DB, DATA_ALL, INIT_HTTP_Q, INIT_SOCKS4_Q,
                               INIT_SOCKS5_Q)
from .items import (ProxyScoreItem, ProxyVerifiedTimeItem, ProxySpeedItem)


class BasePipeline:
    def open_spider(self, spider):
        self.redis_conn = get_redis_conn()

    def process_item(self, item, spider):
        return deferToThread(self._process_item, item, spider)

    def _process_item(self, item, spider):
        raise NotImplementedError


class ProxyIPPipeline(BasePipeline):
    def _process_item(self, item, spider):
        url = item.get('url', None)
        if not url:
            return item

        pipeline = self.redis_conn.pipeline()
        not_exists = pipeline.sadd(DATA_ALL, url)
        if not_exists:
            if 'socks4' in url:
                pipeline.rpush(INIT_SOCKS4_Q, url)
            elif 'socks5' in url:
                pipeline.rpush(INIT_SOCKS5_Q, url)
            else:
                pipeline.rpush(INIT_HTTP_Q, url)
        pipeline.execute()
        return item


class ProxyCommonPipeline(BasePipeline):
    def _process_item(self, item, spider):
        if isinstance(item, ProxyScoreItem):
            self._process_score_item(item, spider)
        if isinstance(item, ProxyVerifiedTimeItem):
            self._process_verified_item(item, spider)
        if isinstance(item, ProxySpeedItem):
            self._process_speed_item(item, spider)

        return item

    def _process_score_item(self, item, spider):
        score = self.redis_conn.zscore(item['queue'], item['url'])
        if score is None:
            self.redis_conn.zadd(item['queue'], {item['url']: item['score']})
        else:
            # delete ip resource when score < 1 or error happens
            if item['incr'] == '-inf' or (item['incr'] < 0 and score <= 1):
                pipe = self.redis_conn.pipeline(True)
                pipe.srem(DATA_ALL, item['url'])
                pipe.zrem(item['queue'], item['url'])
                pipe.execute()
            elif item['incr'] < 0 and 1 < score:
                self.redis_conn.zincrby(item['queue'], -1, item['url'])
            elif item['incr'] > 0 and score < 10:
                self.redis_conn.zincrby(item['queue'], 1, item['url'])
            elif item['incr'] > 0 and score >= 10:
                incr = round(10 / score, 2)
                self.redis_conn.zincrby(item['queue'], incr, item['url'])

    def _process_verified_item(self, item, spider):
        if item['incr'] == '-inf' or item['incr'] < 0:
            raise DropItem('item verification has failed')

        self.redis_conn.zadd(item['queue'],
                             {item['url']: item['verified_time']})

    def _process_speed_item(self, item, spider):
        if item['incr'] == '-inf' or item['incr'] < 0:
            raise DropItem('item verification has failed')

        self.redis_conn.zadd(item['queue'],
                             {item['url']: item['response_time']})
