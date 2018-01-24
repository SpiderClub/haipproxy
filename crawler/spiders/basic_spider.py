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
        # todo register all the website dynamicly
        if 'xdaili' in response.url:
            items = self.parse_json(response, detail_rule=['RESULT', 'rows'])
        elif '66ip' in response.url:
            items = self.parse_common(response, 4)
        elif 'baizhongsou' in response.url:
            items = self.parse_common(response, split_detail=True)
        elif 'coderbusy' in response.url:
            items = self.parse_common(response, ip_pos=1, port_pos=2, extract_protocol=False)
        elif 'data5u' in response.url:
            items = self.parse_common(response, pre_extract='//ul[contains(@class, "l2")]', infos_pos=0,
                                      detail_rule='span li::text')
        elif 'httpsdaili' in response.url or 'yun-daili' in response.url:
            items = self.parse_common(response, pre_extract='//tr[contains(@class, "odd")]', infos_pos=0)
        elif 'ab57' in response.url:
            items = self.parse_raw_text(response)
        elif 'my-proxy' in response.url:
            protocols = None
            if 'socks-4' in response.url:
                protocols = ['socks4']
            if 'socks-5' in response.url:
                protocols = ['socks5']
            items = self.parse_my_proxy(response, pre_extract='.list ::text',
                                        redundancy='#', protocols=protocols)
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





