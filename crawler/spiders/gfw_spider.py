"""
Proxy spider for the websites blocked by gfw.

"""
from config.settings import SPIDER_GFW_TASK
from .basic_spider import CommonSpider


class GFWSpider(CommonSpider):
    name = 'gfw'
    proxy_mode = 2
    task_type = SPIDER_GFW_TASK

    def parse(self, response):
        if 'cn-proxy' in response.url:
            items = self.parse_common(response, pre_extract='//tbody/tr', infos_pos=0)
        elif 'proxylistplus' in response.url:
            protocols = None
            if 'SSL' in response.url:
                protocols = ['https']
            items = self.parse_common(response, pre_extract='//tr[contains(@class, "cells")]',
                                      infos_end=-1, protocols=protocols)
        else:
            items = list()

        for item in items:
            yield item





