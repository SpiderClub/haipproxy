"""
Ajax proxy ip crawler with scrapy-splash
"""
from haipproxy.config.rules import CRAWLER_QUEUE_MAPS
from ..redis_spiders import RedisAjaxSpider
from ..items import ProxyUrlItem
from .base import BaseSpider
from .common_spider import CommonSpider


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


class AjaxGFWSpider(BaseSpider, RedisAjaxSpider):
    name = 'ajax_gfw'
    proxy_mode = 2
    task_queue = CRAWLER_QUEUE_MAPS[name]

    def __init__(self):
        super().__init__()
        self.parser_maps.setdefault('cnproxy', self.parse_cnproxy)
        self.parser_maps.setdefault('free-proxy', self.parse_free_proxy)

    def parse_cnproxy(self, response):
        items = list()
        infos = response.xpath('//tr')[2:]
        for info in infos:
            info_str = info.extract()
            proxy_detail = info.css('td::text').extract()
            ip = proxy_detail[0].strip()
            port = proxy_detail[1][1:].strip()
            cur_protocols = self.procotol_extractor(info_str)
            for protocol in cur_protocols:
                items.append(
                    ProxyUrlItem(
                        url=self.construct_proxy_url(protocol, ip, port)))

        return items

    def parse_free_proxy(self, response):
        items = list()
        infos = response.xpath('//table[@id="proxy_list"]').css('tr')[1:]
        for info in infos:
            info_str = info.extract()
            ip = info.css('abbr::text').extract_first()
            port = info.css('.fport::text').extract_first()
            if not ip or not port:
                continue

            cur_protocols = self.procotol_extractor(info_str)
            for protocol in cur_protocols:
                items.append(
                    ProxyUrlItem(
                        url=self.construct_proxy_url(protocol, ip, port)))

        return items


class GFWSpider(CommonSpider):
    name = 'gfw'
    proxy_mode = 2
    task_queue = CRAWLER_QUEUE_MAPS[name]

    def __init__(self):
        super().__init__()
        self.parser_maps.setdefault('gather_proxy', self.parse_gather_proxy)

    def parse_gather_proxy(self, response):
        items = list()
        infos = response.css('script::text').re(r'gp.insertPrx\((.*)\)')
        for info in infos:
            info = info.lower()
            detail = json.loads(info)
            ip = detail.get('proxy_ip')
            port = detail.get('proxy_port')
            protocols = self.procotol_extractor(info)
            for protocol in protocols:
                items.append(
                    ProxyUrlItem(
                        url=self.construct_proxy_url(protocol, ip, port)))
        return items
