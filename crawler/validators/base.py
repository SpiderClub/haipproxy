"""
Useful base class for all the validators.
"""
import time

from twisted.internet.error import (
    TimeoutError, TCPTimedOutError)

from ..items import (
    ProxyScoreItem, ProxyVerifiedTimeItem,
    ProxySpeedItem)


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
            'crawler.middlewares.RequestStartProfileMiddleware': 500,
            'crawler.middlewares.RequestEndProfileMiddleware': 500,
        },
        'ITEM_PIPELINES': {
            'crawler.pipelines.ProxyCommonPipeline': 200,
        }

    }
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

        items = self.set_item_queue(url, proxy, self.init_score, 1, speed)
        for item in items:
            yield item

    def is_transparent(self, response):
        return False

    def parse_error(self, failure):
        request = failure.request
        proxy = request.meta.get('proxy')
        self.logger.error('proxy {} has been failed,{} is raised'.format(proxy, failure))
        if failure.check(TimeoutError, TCPTimedOutError):
            decr = -1
        else:
            decr = '-inf'

        items = self.set_item_queue(request.url, proxy, self.init_score, decr)
        for item in items:
            yield item

    def set_item_queue(self, url, proxy, score, incr, speed=0):
        score_item = ProxyScoreItem(url=proxy, score=score, incr=incr)
        ttl_item = ProxyVerifiedTimeItem(url=proxy, verified_time=int(time.time()), incr=incr)
        speed_item = ProxySpeedItem(url=proxy, response_time=speed, incr=incr)
        score_item['queue'] = self.score_queue
        ttl_item['queue'] = self.ttl_queue
        speed_item['queue'] = self.speed_queue

        return score_item, ttl_item, speed_item






