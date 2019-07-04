"""
All the spiders are used to validate ip resources.

Here are all the validator websites
https://httpbin.org/ip
http://httpbin.org/ip
https://weibo.cn/

If you want to add your own validators,you must add all the queues
in config/settings.py and register tasks in config/rules.py, and add
the task key to HttpbinValidator's https_tasks or http_tasks
"""
from .httpbin import (HttpbinValidator, HttpValidator, HttpsValidator)
from .zhihu import ZhiHuValidator
from .weibo import WeiBoValidator

all_validators = [
    HttpbinValidator, HttpValidator, HttpsValidator, WeiBoValidator,
    ZhiHuValidator
]
