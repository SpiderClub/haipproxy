"""
We use this validator to filter ip that can access mobile weibo website.
"""
from haipproxy.config.settings import (TEMP_WEIBO_Q, VALIDATED_WEIBO_Q,
                                       TTL_WEIBO_Q, SPEED_WEIBO_Q)
from ..redis_spiders import ValidatorRedisSpider
from .base import BaseValidator


class WeiBoValidator(BaseValidator, ValidatorRedisSpider):
    """This validator checks the liveness of weibo proxy resources"""
    name = 'weibo'
    urls = ['https://weibo.cn/']
    task_queue = TEMP_WEIBO_Q
    score_queue = VALIDATED_WEIBO_Q
    ttl_queue = TTL_WEIBO_Q
    speed_queue = SPEED_WEIBO_Q
    success_key = '微博广场'
