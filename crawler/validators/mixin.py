"""
Useful mixin class for all the validators.
"""
from config.settings import (
    VALIDATED_HTTP_QUEUE, VALIDATED_HTTPS_QUEUE,
    VALIDATED_HTTP_QUEUE_UNSTABLE, VALIDATED_HTTPS_QUEUE_UNSTABLE)
from ..items import ProxyDetailItem


class BaseSpider:
    factor = 10
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
        speed = response.meta.get('speed')
        proxy = response.meta.get('proxy')
        url = response.url
        res = self.parse_detail(response)
        if res:
            if 'https' in url:
                yield ProxyDetailItem(proxy, self.factor, VALIDATED_HTTPS_QUEUE)
            else:
                yield ProxyDetailItem(proxy, self.factor, VALIDATED_HTTP_QUEUE)

    def parse_detail(self, response):
        pass

    def parse_error(self, failure):
        request = failure.request
        proxy = request.meta.get('proxy')
        print('proxy {} has been failed', proxy)
        url = request.url
        if 'https' in url:
            yield ProxyDetailItem(proxy, self.factor/2, VALIDATED_HTTPS_QUEUE_UNSTABLE)
        else:
            yield ProxyDetailItem(proxy, self.factor/2, VALIDATED_HTTP_QUEUE_UNSTABLE)






