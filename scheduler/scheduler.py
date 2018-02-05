"""
This module schedules ip fetching tasks according to config.rules.
"""
from config.rules import URLS
from utils.connetion import get_redis_con
from config.settings import SPIDER_COMMON_TASK


class TaskScheduler:
    @classmethod
    def store_task_into_redis(cls):
        con = get_redis_con()
        for detail in URLS:
            if not detail.get('enable'):
                continue
            task_type = detail.get('task_type', SPIDER_COMMON_TASK)
            url_format = detail.get('url_format')
            # todo split the code into multi functions
            con.lpush(task_type, *url_format)


if __name__ == '__main__':
    TaskScheduler.store_task_into_redis()