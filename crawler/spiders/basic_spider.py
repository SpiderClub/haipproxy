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
        # todo register all the website dynamicly
        if 'xdaili' in response.url:
            items = self.parse_json(response, detail_rule=['RESULT', 'rows'])
        elif '66ip' in response.url:
            items = self.parse_common(response, 4)
        elif 'baizhongsou' in response.url:
            items = self.parse_baizhongsou(response)
        elif 'coderbusy' in response.url:
            items = self.parse_common(response, ip_pos=1, port_pos=2, extract_protocol=False)
        elif 'data5u' in response.url:
            items = self.parse_common(response, pre_extract='//ul[contains(@class, "l2")]', infos_pos=0,
                                      detail_rule='span li::text')
        elif 'httpsdaili' or 'yun-daili' in response.url:
            items = self.parse_common(response, pre_extract='//tr[contains(@class, "odd")]', infos_pos=0)
        else:
            items = self.parse_common(response)

        for item in items:
            yield item

    def parse_baizhongsou(self, response):
        infos = response.xpath('//tr')[1:]
        items = list()
        for info in infos:
            proxy_detail = info.css('td::text').extract()
            if not proxy_detail:
                continue
            ip, port = proxy_detail[0].split(':')
            protocols = self.procotol_extractor(info.extract())
            for protocol in protocols:
                items.append(ProxyUrlItem(url=self.construct_proxy_url(protocol, ip, port)))
        return items





