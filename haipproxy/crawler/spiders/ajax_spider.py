"""
Ajax proxy ip crawler with scrapy-splash
"""
from haipproxy.config.rules import CRAWLER_QUEUE_MAPS
from ..redis_spiders import RedisAjaxSpider
from ..items import ProxyUrlItem
from .base import BaseSpider


class AjaxSpider(BaseSpider, RedisAjaxSpider):
    name = 'ajax'
    task_queue = CRAWLER_QUEUE_MAPS[name]
    custom_settings = {
        'DOWNLOADER_MIDDLEWARES': {
            'haipproxy.crawler.middlewares.RandomUserAgentMiddleware': 543,
            'haipproxy.crawler.middlewares.ProxyMiddleware': 543,
            'scrapy_splash.SplashCookiesMiddleware': 723,
            # it should be prior to HttpProxyMiddleware
            'scrapy_splash.SplashMiddleware': 725,
        },
        'SPIDER_MIDDLEWARES': {
            'scrapy_splash.SplashDeduplicateArgsMiddleware': 100,
        }
    }

    def __init__(self):
        super().__init__()
        self.parser_maps.setdefault('goubanjia', self.parse_goubanjia)

    def parse_goubanjia(self, response):
        infos = response.xpath('//tr')[1:]
        items = list()
        for info in infos:
            proxy_detail = info.xpath(
                'td[1]//*[name(.)!="p"]/text()').extract()
            ip = "".join(proxy_detail[:-1])
            port = proxy_detail[-1]
            protocols = self.procotol_extractor(info.extract())
            for protocol in protocols:
                items.append(
                    ProxyUrlItem(
                        url=self.construct_proxy_url(protocol, ip, port)))
        return items
