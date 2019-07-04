"""
Basic proxy ip crawler.
"""
from urllib.parse import urlparse

import scrapy

from haipproxy.config.rules import CRAWLER_QUEUE_MAPS, PARSE_MAP
from ..redis_spiders import RedisSpider
from ..items import ProxyUrlItem
from .base import BaseSpider


class ProxySpider(scrapy.Spider):
    name = 'proxy'
    custom_settings = {
        'ITEM_PIPELINES': {
            'haipproxy.crawler.pipelines.ProxyIPPipeline': 200,
        },
        'USER_AGENT': 'Mozilla/6.0',
    }

    def start_requests(self):
        urls = [
            'https://www.xicidaili.com/nn/1',
            'https://www.kuaidaili.com/free/inha/1/',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        site = urlparse(response.url).hostname.split('.')[1]
        debug = False
        if debug:
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
            protocol = cols[protocal_pos].xpath('text()').get().lower()
            yield ProxyUrlItem(url=f'{protocol}://{ip}:{port}')


# notice multi inheritance order in python
class CommonSpider(BaseSpider, RedisSpider):
    name = 'common'
    task_queue = CRAWLER_QUEUE_MAPS[name]

    def __init__(self):
        super().__init__()
        self.parser_maps.setdefault('myproxy', self.parse_my_proxy)

    def parse_my_proxy(self, response):
        protocols = None
        if self.exists(response.url, 'socks-4'):
            protocols = ['socks4']
        if self.exists(response.url, 'socks-5'):
            protocols = ['socks5']

        items = list()
        infos = response.css('.list ::text').extract()
        for info in infos:
            if ':' not in info:
                continue
            pos = info.find('#')
            if pos != -1:
                info = info[:info.find('#')]
            ip, port = info.split(':')
            protocols = self.default_protocols if not protocols else protocols
            for protocol in protocols:
                items.append(
                    ProxyUrlItem(
                        url=self.construct_proxy_url(protocol, ip, port)))
        return items
