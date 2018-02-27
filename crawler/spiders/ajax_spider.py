"""
Ajax proxy ip crawler with scrapy-splash
"""
from config.settings import SPIDER_AJAX_TASK
from ..redis_spiders import RedisAjaxSpider
from ..items import ProxyUrlItem
from .base import BaseSpider


class AjaxSpider(BaseSpider, RedisAjaxSpider):
    name = 'ajax'
    task_queue = SPIDER_AJAX_TASK

    def parse(self, response):
        url = response.url
        if self.exists(url, 'goubanjia'):
            items = self.parse_goubanjia(response)
        elif self.exists(url, 'proxydb'):
            items = self.parse_common(response, detail_rule='a::text', split_detail=True)
        elif self.exists(url, 'cool-proxy'):
            items = self.parse_common(response, infos_pos=1, infos_end=-1)
        else:
            items = self.parse_common(response)

        for item in items:
            yield item

    def parse_goubanjia(self, response):
        infos = response.xpath('//tr')[1:]
        items = list()
        for info in infos:
            proxy_detail = info.xpath('td[1]//*[name(.)!="p"]/text()').extract()
            ip = "".join(proxy_detail[:-1])
            port = proxy_detail[-1]
            protocols = self.procotol_extractor(info.extract())
            for protocol in protocols:
                items.append(ProxyUrlItem(url=self.construct_proxy_url(protocol, ip, port)))
        return items





