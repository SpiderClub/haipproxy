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
        'CONCURRENT_REQUESTS_PER_DOMAIN': 1,
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
                    yield ProxyDetailItem(proxy, self.init_score * 0.9, VALIDATED_HTTPS_QUEUE)
                else:
                    yield ProxyDetailItem(proxy, self.init_score * 0.9, VALIDATED_HTTP_QUEUE)
        else:
            score = 0
            if 'https' in url:
                yield ProxyDetailItem(proxy, score, VALIDATED_HTTPS_QUEUE)
            else:
                yield ProxyDetailItem(proxy, score, VALIDATED_HTTP_QUEUE)

    def parse_detail(self, response):
        pass

    def parse_error(self, failure):
        request = failure.request
        proxy = request.meta.get('proxy')
        self.logger.info('proxy {} has been failed', proxy)
        url = request.url
        if 'init' in self.name:
            if 'https' in url:
                yield ProxyDetailItem(proxy, self.init_score * 0.7, VALIDATED_HTTPS_QUEUE)
            else:
                yield ProxyDetailItem(proxy, self.init_score * 0.7, VALIDATED_HTTP_QUEUE)
        else:
            score = 0
            if 'https' in url:
                yield ProxyDetailItem(proxy, score, VALIDATED_HTTPS_QUEUE)
            else:
                yield ProxyDetailItem(proxy, score, VALIDATED_HTTP_QUEUE)






