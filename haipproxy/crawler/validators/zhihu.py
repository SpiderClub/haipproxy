"""
We use this validator to filter ip that can access mobile zhihu website.
"""
from haipproxy.config.settings import (TEMP_ZHIHU_Q, VALIDATED_ZHIHU_Q,
                                       TTL_ZHIHU_Q, SPEED_ZHIHU_Q)
from ..redis_spiders import ValidatorRedisSpider
from .base import BaseValidator


class ZhiHuValidator(BaseValidator, ValidatorRedisSpider):
    """This validator checks the liveness of zhihu proxy resources"""
    name = 'zhihu'
    urls = ['https://www.zhihu.com/question/47464143']
    task_queue = TEMP_ZHIHU_Q
    score_queue = VALIDATED_ZHIHU_Q
    ttl_queue = TTL_ZHIHU_Q
    speed_queue = SPEED_ZHIHU_Q
    success_key = '安全验证'
