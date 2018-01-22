"""
Basic proxy ip crawler.

"""
from config.settings import SPIDER_COMMON_TASK
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
        else:
            items = self.parse_common(response)

        for item in items:
            yield item








