"""
Useful mixin class for all the validators.
"""
from config.settings import (
    VALIDATED_HTTP_QUEUE, VALIDATED_HTTPS_QUEUE)
from ..items import ProxyDetailItem


class BaseValidator:
    """base validator for all the validators"""
    init_score = 10
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
        if 'init' in self.name:
            not_transparent = self.parse_detail(response)
            if not_transparent:
                item = self.set_item_queue(url, proxy, self.init_score * 0.9, 0)
                yield item
        else:
            item = self.set_item_queue(url, proxy, self.init_score * 0.9, 1)
            yield item

    def parse_detail(self, response):
        pass

    def parse_error(self, failure):
        # todo detail with all kinds of errors
        request = failure.request
        proxy = request.meta.get('proxy')
        self.logger.info('proxy {} has been failed'.format(proxy))
        url = request.url
        if 'init' in self.name:
            item = self.set_item_queue(url, proxy, self.init_score * 0.7, 0)
        else:
            item = self.set_item_queue(url, proxy, self.init_score * 0.7, -1)
        yield item

    def set_item_queue(self, url, proxy, score, incr):
        item = ProxyDetailItem(url=proxy, score=score, incr=incr)
        if 'https' in url:
            item['queue'] = VALIDATED_HTTPS_QUEUE
        else:
            item['queue'] = VALIDATED_HTTP_QUEUE
        return item





