"""
Proxy spider for the websites blocked by gfw.
"""
import re
import json

from haipproxy.config.settings import SPIDER_GFW_TASK
from ..items import ProxyUrlItem
from .common_spider import CommonSpider


class GFWSpider(CommonSpider):
    name = 'gfw'
    proxy_mode = 2
    task_queue = SPIDER_GFW_TASK

    def __init__(self):
        super().__init__()
        self.parser_maps.setdefault('xroxy', self.parse_xroxy)
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

    def parse_xroxy(self, response):
        items = list()
        ip_extract_pattern = '">(.*)\\n'
        infos = response.xpath('//tr').css('.row1') + response.xpath(
            '//tr').css('.row0')
        for info in infos:
            m = re.search(ip_extract_pattern, info.css('a')[1].extract())
            if m:
                ip = m.group(1)
                port = info.css('a::text')[2].extract()
                protocol = info.css('a::text')[3].extract().lower()
                if protocol in ['socks4', 'socks5']:
                    items.append(
                        ProxyUrlItem(
                            url=self.construct_proxy_url(protocol, ip, port)))
                elif protocol == 'transparent':
                    continue
                else:
                    items.append(
                        ProxyUrlItem(
                            url=self.construct_proxy_url('http', ip, port)))
                    is_ssl = info.css('a::text')[4].extract().lower() == 'true'
                    if is_ssl:
                        items.append(
                            ProxyUrlItem(url=self.construct_proxy_url(
                                'https', ip, port)))

        return items
