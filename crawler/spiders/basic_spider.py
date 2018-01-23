"""
Basic proxy ip crawler.

"""
from config.settings import SPIDER_COMMON_TASK
from ..items import ProxyUrlItem
from ..redis_spiders import RedisSpider
from .mixin import BaseSpider


# notice multi inheritance order in python
class CommonSpider(BaseSpider, RedisSpider):
    name = 'common'
    task_type = SPIDER_COMMON_TASK

    def parse(self, response):
        if 'xdaili' in response.url:
            items = self.parse_json(response, detail_rule=['RESULT', 'rows'])
        elif '66ip' in response.url:
            items = self.parse_common(response, 4)
        elif 'baizhongsou' in response.url:
            items = self.parse_baizhongsou(response)
        else:
            items = self.parse_common(response)

        for item in items:
            yield item

    def parse_baizhongsou(self, response):
        infos = response.xpath('//tr')[1:]
        items = list()
        for info in infos:
            ip_port = info.css('td::text').extract()
            if not ip_port:
                continue
            ip, port = ip_port[0].split(':')
            protocols = self.procotol_extractor(info.extract())
            for protocol in protocols:
                items.append(ProxyUrlItem(url=self.construct_proxy_url(protocol, ip, port)))
        return items







