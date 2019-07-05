"""
Proxy spider for the websites blocked by gfw.
"""
import re
import json

from haipproxy.config.rules import CRAWLER_QUEUE_MAPS
from ..items import ProxyUrlItem
from .common_spider import CommonSpider


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
