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
            start = detail.get('start', None)
            end = detail.get('end', None)
            url_format = detail.get('url_format')
            task_type = detail.get('task_type', SPIDER_COMMON_TASK)
            if not start and not end:
                con.lpush(task_type, url_format)
            else:
                seeds = [url_format.format(page) for page in range(start, end+1)]
                con.lpush(task_type, *seeds)


if __name__ == '__main__':
    TaskScheduler.store_task_into_redis()