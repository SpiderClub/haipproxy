"""
scrapy pipelines for storing proxy ip infos.
"""
from twisted.internet.threads import deferToThread
from scrapy.exceptions import DropItem

from ..utils import get_redis_conn
from ..config.settings import (REDIS_DB, DATA_ALL, INIT_HTTP_QUEUE,
                               INIT_SOCKS4_QUEUE, INIT_SOCKS5_QUEUE)
from .items import (ProxyScoreItem, ProxyVerifiedTimeItem, ProxySpeedItem)


class BasePipeline:
    def open_spider(self, spider):
        self.redis_con = get_redis_conn(db=REDIS_DB)

    def process_item(self, item, spider):
        return deferToThread(self._process_item, item, spider)

    def _process_item(self, item, spider):
        raise NotImplementedError


class ProxyIPPipeline(BasePipeline):
    def _process_item(self, item, spider):
        url = item.get('url', None)
        if not url:
            return item

        pipeline = self.redis_con.pipeline()
        not_exists = pipeline.sadd(DATA_ALL, url)
        if not_exists:
            if 'socks4' in url:
                pipeline.rpush(INIT_SOCKS4_QUEUE, url)
            elif 'socks5' in url:
                pipeline.rpush(INIT_SOCKS5_QUEUE, url)
            else:
                pipeline.rpush(INIT_HTTP_QUEUE, url)
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
        score = self.redis_con.zscore(item['queue'], item['url'])
        if score is None:
            self.redis_con.zadd(item['queue'],{item['url']: item['score']})
        else:
            # delete ip resource when score < 1 or error happens
            if item['incr'] == '-inf' or (item['incr'] < 0 and score <= 1):
                pipe = self.redis_con.pipeline(True)
                pipe.srem(DATA_ALL, item['url'])
                pipe.zrem(item['queue'], item['url'])
                pipe.execute()
            elif item['incr'] < 0 and 1 < score:
                self.redis_con.zincrby(item['queue'], item['url'], -1)
            elif item['incr'] > 0 and score < 10:
                self.redis_con.zincrby(item['queue'], item['url'], 1)
            elif item['incr'] > 0 and score >= 10:
                incr = round(10 / score, 2)
                self.redis_con.zincrby(item['queue'], item['url'], incr)

    def _process_verified_item(self, item, spider):
        if item['incr'] == '-inf' or item['incr'] < 0:
            raise DropItem('item verification has failed')

        self.redis_con.zadd(item['queue'],{item['url']: item['verified_time']})

    def _process_speed_item(self, item, spider):
        if item['incr'] == '-inf' or item['incr'] < 0:
            raise DropItem('item verification has failed')

        self.redis_con.zadd(item['queue'],{item['url']: item['response_time']})
