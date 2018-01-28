"""
Basic proxy ip crawler.

"""
from config.settings import SPIDER_COMMON_TASK
from ..redis_spiders import RedisSpider
from ..items import ProxyUrlItem
from .mixin import BaseSpider


# notice multi inheritance order in python
class CommonSpider(BaseSpider, RedisSpider):
    name = 'common'
    task_type = SPIDER_COMMON_TASK

    def parse(self, response):
        url = response.url

        if self.exists(url, 'xdaili'):
            items = self.parse_json(response, detail_rule=['RESULT', 'rows'])
        elif self.exists(url, '66ip'):
            items = self.parse_common(response, infos_pos=4)
        elif self.exists(url, 'baizhongsou', 'atomintersoft'):
            items = self.parse_common(response, split_detail=True)
        elif self.exists(url, 'coderbusy'):
            items = self.parse_common(response, ip_pos=1, port_pos=2, extract_protocol=False)
        elif self.exists(url, 'data5u'):
            items = self.parse_common(response, pre_extract='//ul[contains(@class, "l2")]', infos_pos=0,
                                      detail_rule='span li::text')
        elif self.exists(url, 'httpsdaili', 'yun-daili'):
            items = self.parse_common(response, pre_extract='//tr[contains(@class, "odd")]', infos_pos=0)
        elif self.exists(url, 'ab57', 'proxylists'):
            items = self.parse_raw_text(response)
        elif self.exists(url, 'rmccurdy'):
            items = self.parse_raw_text(response, delimiter='\n')
        elif self.exists(url, 'my-proxy'):
            protocols = None
            if self.exists(url, 'socks-4'):
                protocols = ['socks4']
            if self.exists(url, 'socks-5'):
                protocols = ['socks5']
            items = self.parse_my_proxy(response, pre_extract='.list ::text',
                                        redundancy='#', protocols=protocols)
        elif self.exists(url, 'us-proxy', 'free-proxy', 'sslproxies', 'socks-proxy'):
            protocols = None
            if self.exists(url, 'sslproxies'):
                protocols = ['https']
            items = self.parse_common(response, pre_extract='//tbody//tr', infos_pos=0, protocols=protocols)
        elif self.exists(url, 'mrhinkydink'):
            items = self.parse_common(response, pre_extract_method='css', pre_extract='.text', infos_pos=1)
        else:
            items = self.parse_common(response)

        for item in items:
            yield item

    def parse_my_proxy(self, response, pre_extract='.list ::text', redundancy=None, protocols=None):
        items = list()
        infos = response.css(pre_extract).extract()
        for info in infos:
            if ':' not in info:
                continue
            if redundancy:
                pos = info.find(redundancy)
                if pos != -1:
                    info = info[:info.find(redundancy)]

            ip, port = info.split(':')
            protocols = self.default_protocols if not protocols else protocols
            for protocol in protocols:
                items.append(ProxyUrlItem(url=self.construct_proxy_url(protocol, ip, port)))
        return items





