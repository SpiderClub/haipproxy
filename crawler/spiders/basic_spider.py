"""
Basic proxy ip crawler.

"""
from config.settings import SPIDER_COMMON_TASK
from ..redis_spiders import RedisSpider
from ..items import ProxyUrlItem
from .mixin import BaseSpider


# notice multi inheritance order in python
class CommonSpider(BaseSpider, RedisSpider):
    name = 'common'
    task_type = SPIDER_COMMON_TASK

    def parse(self, response):
        infos = response.xpath('//tr')[1:]
        for info in infos:
            proxy_detail = info.css('td::text').extract()
            ip = proxy_detail[0]
            port = proxy_detail[1]
            detail = ''.join(proxy_detail).lower()
            protocols = self.procotol_extractor(detail)

            for protocol in protocols:
                yield ProxyUrlItem(url=self.construct_proxy_url(protocol, ip, port))






