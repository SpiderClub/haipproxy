"""
Proxy spider for the websites blocked by gfw.

"""
import json

from config.settings import SPIDER_GFW_TASK
from ..items import ProxyUrlItem
from .basic_spider import CommonSpider


class GFWSpider(CommonSpider):
    name = 'gfw'
    proxy_mode = 2
    task_type = SPIDER_GFW_TASK

    def parse(self, response):
        if 'cn-proxy' in response.url:
            items = self.parse_common(response, pre_extract='//tbody/tr', infos_pos=0)
        elif 'proxylistplus' in response.url:
            protocols = None
            if 'SSL' in response.url:
                protocols = ['https']
            items = self.parse_common(response, pre_extract='//tr[contains(@class, "cells")]',
                                      infos_end=-1, protocols=protocols)
        elif 'gatherproxy' in response.url:
            items = self.parse_gather_proxy(response)
        else:
            items = list()

        for item in items:
            yield item

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
                items.append(ProxyUrlItem(url=self.construct_proxy_url(protocol, ip, port)))
        return items

    def parse_proxylist_proxy(self, response):
        items = list()
        infos = response.css('script::text').re(r'gp.insertPrx\((.*)\)')
        for info in infos:
            info = info.lower()
            detail = json.loads(info)
            ip = detail.get('proxy_ip')
            port = detail.get('proxy_port')
            protocols = self.procotol_extractor(info)
            for protocol in protocols:
                items.append(ProxyUrlItem(url=self.construct_proxy_url(protocol, ip, port)))
        return items





