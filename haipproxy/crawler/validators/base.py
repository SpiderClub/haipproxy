"""
Useful base class for all the validators.
"""
import logging
import time

from twisted.internet.error import (TimeoutError, TCPTimedOutError)

# from logger import crawler_logger
from ..items import (ProxyScoreItem, ProxyVerifiedTimeItem, ProxySpeedItem)

logger = logging.getLogger(__name__)


class BaseValidator:
    """base validator for all the validators"""
    name = 'base'
    init_score = 5
    # slow down each spider
    custom_settings = {
        'CONCURRENT_REQUESTS': 50,
        'CONCURRENT_REQUESTS_PER_DOMAIN': 50,
        'RETRY_ENABLED': False,
        'DOWNLOADER_MIDDLEWARES': {
            'haipproxy.crawler.middlewares.RequestStartProfileMiddleware': 500,
            'haipproxy.crawler.middlewares.RequestEndProfileMiddleware': 500,
        },
        'ITEM_PIPELINES': {
            'haipproxy.crawler.pipelines.ProxyCommonPipeline': 200,
        }
    }
    use_set = True
    success_key = ''
    # all the children validators must specify the following args
    # unless you overwrite the set_item_queue() method
    urls = None
    task_queue = None
    score_queue = None
    ttl_queue = None
    speed_queue = None

    def parse(self, response):
        proxy = response.meta.get('proxy')
        speed = response.meta.get('speed')
        url = response.url
        transparent = self.is_transparent(response)
        if transparent:
            return
        incr = 1 if self.is_ok(response) else '-inf'
        items = self.set_item_queue(url, proxy, self.init_score, incr, speed)
        for item in items:
            yield item

    def is_transparent(self, response):
        return False

    def parse_error(self, failure):
        request = failure.request
        proxy = request.meta.get('proxy')
        logger.error('proxy {} has failed, {} is raised'.format(proxy, failure))
        if failure.check(TimeoutError, TCPTimedOutError):
            decr = -1
        else:
            decr = '-inf'

        items = self.set_item_queue(request.url, proxy, self.init_score, decr)
        for item in items:
            yield item

    def is_ok(self, response):
        return self.success_key in response.text

    def set_item_queue(self, url, proxy, score, incr, speed=0):
        score_item = ProxyScoreItem(url=proxy, score=score, incr=incr)
        ttl_item = ProxyVerifiedTimeItem(url=proxy,
                                         verified_time=int(time.time()),
                                         incr=incr)
        speed_item = ProxySpeedItem(url=proxy, response_time=speed, incr=incr)
        score_item['queue'] = self.score_queue
        ttl_item['queue'] = self.ttl_queue
        speed_item['queue'] = self.speed_queue

        return score_item, ttl_item, speed_item
