"""
Proxy spider for the websites blocked by gfw.

"""
import re
import json

from config.settings import SPIDER_GFW_TASK
from ..items import ProxyUrlItem
from .basic_spider import CommonSpider


class GFWSpider(CommonSpider):
    name = 'gfw'
    proxy_mode = 2
    task_type = SPIDER_GFW_TASK

    def parse(self, response):
        url = response.url
        if self.exists(url, 'cn-proxy'):
            items = self.parse_common(response, pre_extract='//tbody/tr', infos_pos=0)
        elif self.exists(url, 'proxylistplus'):
            protocols = None
            if self.exists(url, 'SSL'):
                protocols = ['https']
            items = self.parse_common(response, pre_extract='//tr[contains(@class, "cells")]',
                                      infos_end=-1, protocols=protocols)
        elif self.exists(url, 'gatherproxy'):
            items = self.parse_gather_proxy(response)
        elif self.exists(url, 'xroxy'):
            items = self.parse_xroxy(response)
        else:
            items = self.parse_common(response)

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

    def parse_xroxy(self, response):
        items = list()
        ip_extract_pattern = '">(.*)\\n'
        infos = response.xpath('//tr').css('.row1') + response.xpath('//tr').css('.row0')
        for info in infos:
            m = re.search(ip_extract_pattern, info.css('a')[1].extract())
            if m:
                ip = m.group(1)
                port = info.css('a::text')[2].extract()
                protocol = info.css('a::text')[3].extract().lower()
                if protocol in ['socks4', 'socks5']:
                    items.append(ProxyUrlItem(url=self.construct_proxy_url(protocol, ip, port)))
                elif protocol == 'transparent':
                    continue
                else:
                    items.append(ProxyUrlItem(url=self.construct_proxy_url('http', ip, port)))
                    is_ssl = info.css('a::text')[4].extract().lower() == 'true'
                    if is_ssl:
                        items.append(ProxyUrlItem(url=self.construct_proxy_url('https', ip, port)))

        return items







