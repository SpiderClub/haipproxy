"""
Ajax proxy ip crawler with scrapy-splash
"""
from config.settings import SPIDER_AJAX_TASK
from ..redis_spiders import RedisAjaxSpider
from ..items import ProxyUrlItem
from .mixin import BaseSpider


class AjaxSpider(BaseSpider, RedisAjaxSpider):
    name = 'ajax'
    task_type = SPIDER_AJAX_TASK

    def parse(self, response):
        if 'goubanjia' in response.url:
            items = self.parse_goubanjia(response)
        else:
            items = list()

        for item in items:
            yield item

    def parse_goubanjia(self, response):
        infos = response.xpath('//tr')[1:]
        items = list()
        for info in infos:
            ip_port = info.xpath('td[1]//*[name(.)!="p"]/text()').extract()
            ip = "".join(ip_port[:-1])
            port = ip_port[-1]
            protocols = self.procotol_extractor(info.extract())
            for protocol in protocols:
                items.append(ProxyUrlItem(url=self.construct_proxy_url(protocol, ip, port)))
        return items





