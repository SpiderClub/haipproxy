"""
Basic proxy ip crawler.
"""
import logging
from urllib.parse import urlparse

import scrapy
from scrapy_splash.request import SplashRequest

from haipproxy.config.settings import MIN_PROXY_LEN
from haipproxy.crawler.items import ProxyUrlItem
from haipproxy.utils import is_valid_proxy
from .base import BaseSpider
from .redis_spiders import RedisSpider

logger = logging.getLogger(__name__)

PROXY_SITES = {
    'ip3366': {
        'protocal_pos': 3,
        'urls':
        [f'http://www.ip3366.net/free/?stype=1&page={i}' for i in range(1, 8)],
    },
    'kuaidaili': {
        'protocal_pos': 3,
        'urls': [f'https://www.kuaidaili.com/free/inha/{i}/'
         for i in range(1, 21)],  # 2000
    },
    'kxdaili': {
        'protocal_pos': 3,
        'urls': [
            f'http://ip.kxdaili.com/dailiip/{i}/{j}.html#ip'
            for i in range(1, 3) for j in range(1, 5)
        ],
    },
    'mrhinkydink': {
        'row_xpath': '//table/tr[@class="text"]',
        'protocal_pos': -1,
        'urls': ['http://www.mrhinkydink.com/proxies.htm'] +
        [f'http://www.mrhinkydink.com/proxies{i}.htm' for i in range(2, 4)],
    },
    'us-proxy': {
        'protocal_pos': -1,
        'urls': ['https://www.us-proxy.org/'],
    },
    'xicidaili': {
        'row_xpath': '//table/tr[@class]',
        'ip_pos': 1,
        'port_pos': 2,
        'protocal_pos': 5,
        'urls': [f'https://www.xicidaili.com/nn/{i}' for i in range(1, 26)],  # 3000
    },
    'xroxy': {
        'row_xpath': '//table[@id="DataTables_Table_0"]/tbody/tr',
        'protocal_pos': -1,
        'urls': [
            'https://www.xroxy.com/free-proxy-lists/?port=&type=Not_transparent&ssl=&country=&latency=&reliability=2500'
        ],
    },
}
# 'http://tools.rosinstrument.com/raw_free_db.htm?0&t=1'


class ProxySpider(scrapy.Spider):
    name = 'proxy'
    custom_settings = {
        'ITEM_PIPELINES': {
            'haipproxy.crawler.pipelines.ProxyIPPipeline': 200,
        },
        'AJAXCRAWL_ENABLED': True
    }
    default_protocols = ['http', 'https']

    def start_requests(self):
        ajax_urls = []
        text_urls = [
            'http://ab57.ru/downloads/proxyold.txt',
            'http://www.proxylists.net/http_highanon.txt',
            'https://api.proxyscrape.com/?request=getproxies&proxytype=http',
            'https://www.rmccurdy.com/scripts/proxy/good.txt',
        ]
        # If test_urls is not empty, this spider will crawler test_urls ONLY
        test_urls = []
        if test_urls:
            for url in test_urls:
                yield scrapy.Request(url=url, callback=self.parse)
            return
        for _, site in PROXY_SITES.items():
            urls = site.get('urls', [])
            for url in urls:
                yield scrapy.Request(url=url, callback=self.parse)
        for url in text_urls:
            yield scrapy.Request(url=url, callback=self.parse_text)
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
        row_xpath = PROXY_SITES[site].get('row_xpath', '//table/tbody/tr')
        col_xpath = PROXY_SITES[site].get('col_xpath', 'td')
        ip_pos = PROXY_SITES[site].get('ip_pos', 0)
        port_pos = PROXY_SITES[site].get('port_pos', 1)
        protocal_pos = PROXY_SITES[site].get('protocal_pos', 2)
        for row in response.xpath(row_xpath):
            if 'ransparent' in row.get() or '透明' in row.get():
                logger.debug(f'Transparent proxy here: {row.get()}')
                continue
            cols = row.xpath(col_xpath)
            if len(cols) < 3:
                logger.warning(f'Invalid cols: {cols}')
                continue
            ip = cols[ip_pos].xpath('text()').get()
            port = cols[port_pos].xpath('text()').get()
            pro_str = '' if protocal_pos == -1 else cols[protocal_pos].xpath(
                'text()').get().lower()
            for protocol in self.get_protocols(pro_str):
                if is_valid_proxy(ip, port, protocol):
                    yield ProxyUrlItem(url=f'{protocol}://{ip}:{port}')
                else:
                    self.logger.error(
                        f'invalid proxy: {protocol}://{ip}:{port}')

    def parse_text(self, response):
        for line in response.text.split('\n'):
            line = line.strip()
            if len(line) < MIN_PROXY_LEN:
                continue
            proxies = []
            if line[0].isdigit():
                for protocol in self.default_protocols:
                    proxies.append(protocol + '://' + line)
            elif line[0].lower == 'h':
                proxies.append(line)
            else:
                logger.warning(f'Not http(s) proxy: {line}')
            for p in proxies:
                if is_valid_proxy(proxy=p):
                    yield ProxyUrlItem(url=p)

    def get_protocols(self, protocol):
        if not protocol or '' == protocol:
            return self.default_protocols
        elif ',' in protocol:
            return protocol.split(',')
        elif '4/5' in protocol:
            return ['sock4', 'sock5']
        else:
            return [protocol]


class CommonSpider(BaseSpider):
    pass
