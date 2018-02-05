"""
scrapy pipelines for storing proxy ip infos.
"""
from twisted.internet.threads import deferToThread

from utils.redis_util import get_redis_con
from config.settings import (
    META_DATA_DB, DATA_ALL, HTTP_QUEUE, SOCKS4_QUEUE, SOCKS5_QUEUE)


class ProxyIPPipeline:
    def open_spider(self, spider):
        self.redis_con = get_redis_con(db=META_DATA_DB)

    def process_item(self, item, spider):
        return deferToThread(self._process_item, item, spider)

    def _process_item(self, item, spider):
        url = item.get('url', None)
        if not url:
            return item

        pipeline = self.redis_con.pipeline()
        not_exists = pipeline.sadd(DATA_ALL, url)
        if not_exists:
            if 'socks4' in url:
                pipeline.rpush(SOCKS4_QUEUE, url)
            elif 'socks5' in url:
                pipeline.rpush(SOCKS5_QUEUE, url)
            else:
                pipeline.rpush(HTTP_QUEUE, url)
        pipeline.execute()
        return item


class ProxyDetailPipeline:
    def open_spider(self, spider):
        self.redis_con = get_redis_con(db=META_DATA_DB)

    def process_item(self, item, spider):
        return deferToThread(self._process_item, item, spider)

    def _process_item(self, item, spider):
        score = self.redis_con.zscore(item['queue'], item['url'])
        if not item['incr'] or score is None:
            self.redis_con.zadd(item['queue'], item['score'], item['url'])
        else:
            if item['incr'] > 0 and score >= 10:
                incr = round(10/score, 2)
                self.redis_con.zincrby(item['queue'], item['url'], incr)
            elif item['incr'] > 0 and score < 10:
                self.redis_con.zincrby(item['queue'], item['url'], 1)
            elif item['incr'] < 0 and 0 < score:
                self.redis_con.zincrby(item['queue'], item['url'], -1)
            elif item['incr'] < 0 and score <= 0:
                pipe = self.redis_con.pipeline(True)
                pipe.srem(DATA_ALL, item['url'])
                pipe.redis_con.zrem(item['queue'], item['url'])
                pipe.execute()

        return item


