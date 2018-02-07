"""
We use this validator to filter ip that can access weibo
initially score.
"""
from ..redis_spiders import ValidatorRedisSpider
from .mixin import BaseValidator


class WeiBoValidator(BaseValidator, ValidatorRedisSpider):
    name = 'weibo'
    urls = [
        'https://weibo.com'
    ]



