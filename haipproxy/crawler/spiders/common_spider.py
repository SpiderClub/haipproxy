"""
Basic proxy ip crawler.
"""
from urllib.parse import urlparse

import scrapy

from haipproxy.config.rules import CRAWLER_QUEUE_MAPS
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
        cur_parse = getattr(self, f'parse_{site}')
        debug = False
        if debug:
            from scrapy.shell import inspect_response
            inspect_response(response, self)
        for item in cur_parse(response):
            yield item

    def parse_xicidaili(self, response):
        rows = response.xpath('//table/tr[@class]')
        for row in rows:
            cols = row.xpath('td/text()').getall()
            ip = cols[0]
            port = cols[1]
            protocol = cols[5]
            yield ProxyUrlItem(url=f'{protocol}://{ip}:{port}')

    def parse_kuaidaili(self, response):
        rows = response.xpath('//table/tbody/tr')
        for row in rows:
            cols = row.xpath('td/text()').getall()
            ip = cols[0]
            port = cols[1]
            protocol = cols[3]
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
