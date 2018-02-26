"""
Useful mixin class for all the validators.
"""
import time

from twisted.internet.error import (
    TimeoutError, TCPTimedOutError)

from config.settings import (
    VALIDATED_HTTP_QUEUE, VALIDATED_HTTPS_QUEUE,
    TTL_HTTPS_QUEUE, TTL_HTTP_QUEUE)
from ..items import (
    ProxyDetailItem, ProxyVerifiedTimeItem)


class BaseValidator:
    """base validator for all the validators"""
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
            'crawler.pipelines.ProxyDetailPipeline': 200,
        }

    }

    def parse(self, response):
        # don't consider speed at first
        proxy = response.meta.get('proxy')
        url = response.url
        transparent = self.is_transparent(response)
        if transparent:
            return

        items = self.set_item_queue(url, proxy, self.init_score, 1)
        for item in items:
            yield item

    def is_transparent(self, response):
        return False

    def parse_error(self, failure):
        """"""
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

    def set_item_queue(self, url, proxy, score, incr):
        proxy_item = ProxyDetailItem(url=proxy, score=score, incr=incr)
        time_item = ProxyVerifiedTimeItem(url=proxy, verified_time=int(time.time()), incr=incr)
        # todo find a better way to distinguish each task queue,
        # may split the set_item_queue method from basevalidator to each child validtor
        if 'https' in url:
            proxy_item['queue'] = VALIDATED_HTTPS_QUEUE
            time_item['queue'] = TTL_HTTPS_QUEUE
        else:
            proxy_item['queue'] = VALIDATED_HTTP_QUEUE
            time_item['queue'] = TTL_HTTP_QUEUE
        return proxy_item, time_item





