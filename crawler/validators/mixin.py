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
        'CONCURRENT_REQUESTS_PER_DOMAIN': 30,
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
                if 'https' in url:
                    yield ProxyDetailItem(url=proxy, score=self.init_score * 0.9, queue=VALIDATED_HTTPS_QUEUE)
                else:
                    yield ProxyDetailItem(url=proxy, score=self.init_score * 0.9, queue=VALIDATED_HTTP_QUEUE)
        else:
            if 'https' in url:
                yield ProxyDetailItem(url=proxy, score='incr', queue=VALIDATED_HTTPS_QUEUE)
            else:
                yield ProxyDetailItem(url=proxy, score='incr', queue=VALIDATED_HTTP_QUEUE)

    def parse_detail(self, response):
        pass

    def parse_error(self, failure):
        request = failure.request
        proxy = request.meta.get('proxy')
        self.logger.info('proxy {} has been failed'.format(proxy))
        url = request.url
        if 'init' in self.name:
            if 'https' in url:
                yield ProxyDetailItem(url=proxy, score=self.init_score * 0.7, queue=VALIDATED_HTTPS_QUEUE)
            else:
                yield ProxyDetailItem(url=proxy, score=self.init_score * 0.7, queue=VALIDATED_HTTP_QUEUE)
        else:
            if 'https' in url:
                yield ProxyDetailItem(url=proxy, score='decr', queue=VALIDATED_HTTPS_QUEUE)
            else:
                yield ProxyDetailItem(url=proxy, score='decr', queue=VALIDATED_HTTP_QUEUE)






