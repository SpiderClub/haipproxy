"""
Basic proxy ip crawler.
"""
import ipaddress
from urllib.parse import urlparse

import scrapy
from scrapy_splash.request import SplashRequest

from haipproxy.config.rules import PARSE_MAP
from ..redis_spiders import RedisSpider
from ..items import ProxyUrlItem
from .base import BaseSpider


class ProxySpider(scrapy.Spider):
    name = 'proxy'
    custom_settings = {
        'ITEM_PIPELINES': {
            'haipproxy.crawler.pipelines.ProxyIPPipeline': 200,
        },
        'AJAXCRAWL_ENABLED': True
    }

    def start_requests(self):
        urls = [
            'https://www.xicidaili.com/nn/1',
            'https://www.kuaidaili.com/free/inha/1/',
            'http://ip.kxdaili.com/dailiip/1/1.html#ip',
            'http://ip.kxdaili.com/dailiip/2/1.html#ip',
            'https://www.xroxy.com/free-proxy-lists/?port=&type=Not_transparent&ssl=&country=&latency=&reliability=2500',
        ]
        ajax_urls = []
        # If test_urls is not empty, this spider will crawler test_urls ONLY
        test_urls = []
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)
        for url in ajax_urls:
            yield SplashRequest(url=url, callback=self.parse)

    def parse(self, response):
        site = urlparse(response.url).hostname.split('.')[1]
        debug = False
        if debug:
            from scrapy.utils.response import open_in_browser
            open_in_browser(response)
            from scrapy.shell import inspect_response
            inspect_response(response, self)
        row_xpath = PARSE_MAP[site].get('row_xpath', '//table/tbody/tr')
        col_xpath = PARSE_MAP[site].get('col_xpath', 'td')
        ip_pos = PARSE_MAP[site].get('ip_pos', 0)
        port_pos = PARSE_MAP[site].get('port_pos', 1)
        protocal_pos = PARSE_MAP[site].get('protocal_pos', 2)
        rows = response.xpath(row_xpath)
        for row in rows:
            cols = row.xpath(col_xpath)
            ip = cols[ip_pos].xpath('text()').get()
            port = cols[port_pos].xpath('text()').get()
            for protocol in self.get_protocols(
                    cols[protocal_pos].xpath('text()').get().lower()):
                if self.is_valid_proxy(ip, port, protocol):
                    yield ProxyUrlItem(url=f'{protocol}://{ip}:{port}')
                else:
                    self.logger.error(
                        f'invalid proxy: {protocol}://{ip}:{port}')

    def get_protocols(self, protocol):
        if ',' in protocol:
            return protocol.split(',')
        elif '4/5' in protocol:
            return ['sock4', 'sock5']
        elif protocol in ['distorting', 'anonymous']:
            return ['http', 'https']
        else:
            return [protocol]

    def is_valid_proxy(self, ip, port, protocol):
        try:
            ipaddress.ip_address(ip)
        except:
            return False
        return 0 <= int(port) and int(port) <= 65535 and protocol in [
            'http', 'https', 'sock4', 'sock5'
        ]


class CommonSpider(BaseSpider):
    pass
