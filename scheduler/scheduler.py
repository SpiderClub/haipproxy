"""
This module schedules all the tasks according to config.rules.
"""
import time
from multiprocessing import Pool

import schedule

from config.rules import CRWALER_TASKS
from config.settings import (
    SPIDER_COMMON_TASK, TIMER_RECORDER)
from utils.redis_util import (
    get_redis_con, acquire_lock, release_lock)


class TaskScheduler:
    def __init__(self, name):
        self.name = name

    def schedule_with_delay(self):
        for task in CRWALER_TASKS:
            internal = task.get('internal')
            schedule.every(internal).minutes.do(self.schedule_task_with_lock, task)
        while True:
            schedule.run_pending()
            time.sleep(1)

    def schedule_all_right_now(self):
        with Pool() as pool:
            pool.map(self.schedule_task_with_lock, CRWALER_TASKS)

    def schedule_task_with_lock(self, task):
        if not task.get('enable'):
            return None

        conn = get_redis_con()
        task_name = task.get('name')
        internal = task.get('internal')
        task_type = task.get('task_type', SPIDER_COMMON_TASK)
        urls = task.get('url')
        lock_indentifier = acquire_lock(conn, task_name)
        if not lock_indentifier:
            return False
        pipe = conn.pipeline(True)
        try:
            now = int(time.time())
            pipe.hget(TIMER_RECORDER, task_name)
            r = pipe.execute()[0]
            if not r or (now - int(r.decode('utf-8'))) >= internal * 60:
                pipe.lpush(task_type, *urls)
                pipe.hset(TIMER_RECORDER, task_name, now)
                pipe.execute()
                print('task {} has been stored into redis successfully'.format(task_name))
                return True
            else:
                return None
        finally:
            release_lock(conn, task_name, lock_indentifier)



