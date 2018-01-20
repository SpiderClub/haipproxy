"""
Common ip proxy spider
"""
from ..redis_spiders import RedisSpider
from ..items import (
    ProxyIPItem, ProxyUrlItem)
from .mixin import IPSourceMixin


# notice multi inheritance order in python
class CommonSpider(IPSourceMixin, RedisSpider):
    name = 'common'
    # slow down each spider
    custom_settings = {
        'CONCURRENT_REQUESTS_PER_DOMAIN': 1,
        'DOWNLOAD_DELAY': 3
    }

    def parse(self, response):
        infos = response.xpath('//tr')[1:]
        for info in infos:
            proxy_detail = info.css('td::text').extract()
            ip = proxy_detail[0]
            port = proxy_detail[1]
            detail = ''.join(proxy_detail).lower()
            protocols = self.procotol_extractor(detail)

            for protocol in protocols:
                yield ProxyIPItem({
                    'ip': ip,
                    'port': port,
                    'protocol': protocol,
                })
                yield ProxyUrlItem(url=self.construct_proxy_url(protocol, ip, port))

    def procotol_extractor(self, detail):
        # TODO it might be socks4, fix this case
        if 'socks' in detail:
            protocols = ['socks5']
        # TODO find a better way to recongnize http and https protocol
        elif 'http,https' in detail:
            protocols = ['http', 'https']
        elif 'https' in detail:
            protocols = ['https']
        else:
            protocols = ['http']

        return protocols






