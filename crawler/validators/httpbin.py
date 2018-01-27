"""
We use this validator to filter transparent ips, and give the ip resources a
initially score.
"""
import json

from config.settings import (
    HTTP_QUEUE, HTTPS_QUEUE
)

from ..redis_spiders import ValidatorRedisSpider
from .mixin import BaseSpider


class HttpBinSpider(BaseSpider, ValidatorRedisSpider):
    name = 'httpbin'
    urls = {
        HTTP_QUEUE: 'http://httpbin.org/ip',
        HTTPS_QUEUE: 'http://httpbin.org/ip',
    }

    def parse_detail(self, response):
        ip = json.loads(response.body_as_unicode()).get('origin')
        print(ip)




