"""
scrapy pipelines for storing proxy ip infos.
"""
import logging
import time

from haipproxy.utils import RedisOps

logger = logging.getLogger(__name__)


class BasePipeline:
    def open_spider(self, spider):
        self.ro = RedisOps()
    def close_spider(self, spider):
        self.ro.flush()


class ProxyIPPipeline(BasePipeline):
    def process_item(self, item, spider):
        proxy = item.get('url', None)
        self.ro.set_proxy(proxy)
        return item


class ProxyStatPipeline(BasePipeline):
    def process_item(self, item, spider):
        self.ro.inc_stat(item)
        return item
