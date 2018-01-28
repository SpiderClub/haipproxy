"""
We use this validator to filter ip that can access weibo
initially score.
"""
from ..redis_spiders import ValidatorRedisSpider
from .mixin import BaseSpider


class WeiBoValidator(BaseSpider, ValidatorRedisSpider):
    name = 'weibo'
    urls = [
        'http://weibo.com',
        'https://weibo.com'
    ]



