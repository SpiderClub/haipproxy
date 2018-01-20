"""
This module schedules ip fetching tasks according to config.rules.
"""
from config.rules import URLS
from config.settings import SPIDER_TASK_QUEUE
from utils.connetion import get_redis_con


class TaskScheduler:
    @classmethod
    def store_task_into_redis(cls):
        con = get_redis_con()
        seeds = list()
        for detail in URLS:
            if not detail.get('enable'):
                continue
            start = detail.get('start', 1)
            end = detail.get('end', 10)
            url_format = detail.get('url_format')
            seeds.extend(url_format.format(page) for page in range(start, end+1))
        con.lpush(SPIDER_TASK_QUEUE, *seeds)


if __name__ == '__main__':
    TaskScheduler.store_task_into_redis()