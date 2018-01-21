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
            task_type = detail.get('task_type', SPIDER_COMMON_TASK)
            url_format = detail.get('url_format')
            if not start and not end:
                print(*url_format)
                con.lpush(task_type, *url_format)
            else:
                for each in url_format:
                    seeds = [each.format(page) for page in range(start, end+1)]
                    print(*seeds)
                    con.lpush(task_type, *seeds)


if __name__ == '__main__':
    TaskScheduler.store_task_into_redis()