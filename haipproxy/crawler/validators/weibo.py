"""
We use this validator to filter ip that can access mobile weibo website.
"""
from haipproxy.config.settings import (
    TEMP_WEIBO_QUEUE, VALIDATED_WEIBO_QUEUE,
    TTL_WEIBO_QUEUE, SPEED_WEIBO_QUEUE)
from ..redis_spiders import ValidatorRedisSpider
from .base import BaseValidator


class WeiBoValidator(BaseValidator, ValidatorRedisSpider):
    """This validator checks the liveness of weibo proxy resources"""
    name = 'weibo'
    urls = [
        'https://weibo.cn/'
    ]
    task_queue = TEMP_WEIBO_QUEUE
    score_queue = VALIDATED_WEIBO_QUEUE
    ttl_queue = TTL_WEIBO_QUEUE
    speed_queue = SPEED_WEIBO_QUEUE
    success_key = '微博广场'
