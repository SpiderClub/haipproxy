"""
Ajax gfw proxy ip crawler with scrapy-splash
"""
from config.settings import SPIDER_AJAX_GFW_TASK
from ..redis_spiders import RedisAjaxSpider
from .mixin import BaseSpider


class AjaxGFWSpider(BaseSpider, RedisAjaxSpider):
    name = 'ajax_gfw'
    proxy_mode = 2
    task_type = SPIDER_AJAX_GFW_TASK

    def parse(self, response):
        print(response.url)
        items = self.parse_common(response, pre_extract_method='css', pre_extract='.table ul',
                                  detail_rule='li::text', split_detail=True)

        for item in items:
            yield item






