"""
scrapy pipelines for storing proxy ip infos.
"""
from twisted.internet.threads import deferToThread

from utils.connetion import get_redis_con
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

        not_exists = self.redis_con.sadd(DATA_ALL, url)
        if not_exists:
            if 'socks4' in url:
                self.redis_con.sadd(SOCKS4_QUEUE, url)
            elif 'socks5' in url:
                self.redis_con.sadd(SOCKS5_QUEUE, url)
            else:
                self.redis_con.sadd(HTTP_QUEUE, url)
        return item


class ProxyDetailPipeline:
    def open_spider(self, spider):
        self.redis_con = get_redis_con(db=META_DATA_DB)

    def process_item(self, item, spider):
        return deferToThread(self._process_item, item, spider)

    def _process_item(self, item, spider):
        self.redis_con.zadd(item.queue, item.score, item.url)
        return item


