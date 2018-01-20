"""
scrapy pipelines for storing proxy ip infos.
"""
from twisted.internet.threads import deferToThread
from scrapy.utils.serialize import ScrapyJSONEncoder

from config.settings import META_DATA_DB
from utils.connetion import get_redis_con


serialize = ScrapyJSONEncoder().encode


class ProxyIPPipeline:
    def open_spider(self, spider):
        self.redis_con = get_redis_con(db=META_DATA_DB)

    def process_item(self, item, spider):
        return deferToThread(self._process_item, item, spider)

    def _process_item(self, item, spider):
        serialized_item = serialize(item)
        self.redis_con.rpush('to_think', serialized_item)
        return item


