"""
This module schedules all the tasks according to config.rules.
"""
import click
import logging
import multiprocessing
import schedule
import time

from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings
from twisted.internet import reactor

from haipproxy.client import SquidClient
from haipproxy.config.rules import CRAWLER_TASKS, CRAWLER_QUEUE_MAPS
from haipproxy.crawler.spiders import all_spiders
from haipproxy.config.settings import (
    SPIDER_AJAX_Q,
    SPIDER_GFW_Q,
    SPIDER_AJAX_GFW_Q,
    TIMER_RECORDER,
)
from haipproxy.utils import get_redis_conn, acquire_lock, release_lock

DEFAULT_CRAWLER_QS = [SPIDER_AJAX_Q, SPIDER_GFW_Q, SPIDER_AJAX_GFW_Q]

logger = logging.getLogger(__name__)


class BaseScheduler:
    def __init__(self, tasks):
        """
        init function for schedulers.
        :param name: scheduler name, generally the value is used by the scheduler
        :param tasks: tasks in config.rules
        """
        self.tasks = tasks

    def schedule_with_delay(self):
        for task in self.tasks:
            interval = task.get("interval")
            schedule.every(interval).minutes.do(self.schedule_task_with_lock, task)
        while True:
            schedule.run_pending()
            time.sleep(1)

    def schedule_all_right_now(self):
        with multiprocessing.Pool() as pool:
            pool.map(self.schedule_task_with_lock, self.tasks)

    def get_lock(self, redis_conn, task):
        if not task.get("enable"):
            return None

        task_name = task.get("name")
        lock_indentifier = acquire_lock(redis_conn, task_name)
        return lock_indentifier

    def schedule_task_with_lock(self, task):
        raise NotImplementedError


class CrawlerScheduler(BaseScheduler):
    def schedule_task_with_lock(self, task):
        """Crawler scheduler filters tasks according to task type"""
        task_name = task.get("name")
        if not task.get("enable"):
            return None
        task_queue = CRAWLER_QUEUE_MAPS[task_name]

        redis_conn = get_redis_conn()
        interval = task.get("interval")
        urls = task.get("resource")
        lock_indentifier = acquire_lock(redis_conn, task_name)
        if not lock_indentifier:
            return False

        pipe = redis_conn.pipeline(True)
        try:
            now = int(time.time())
            pipe.hget(TIMER_RECORDER, task_name)
            r = pipe.execute()[0]
            if not r or (now - int(r.decode("utf-8"))) >= interval * 60:
                pipe.lpush(task_queue, *urls)
                pipe.hset(TIMER_RECORDER, task_name, now)
                pipe.execute()
                logger.info(
                    "crawler task {} has been stored into redis successfully".format(
                        task_name
                    )
                )
                return True
            else:
                return None
        finally:
            release_lock(redis_conn, task_name, lock_indentifier)


def scheduler_start(tasks):
    """Start specified scheduler."""
    default_tasks = CRAWLER_TASKS
    SchedulerCls = CrawlerScheduler

    scheduler = SchedulerCls(default_tasks)
    scheduler.schedule_all_right_now()
    scheduler.schedule_with_delay()


def crawler_start(tasks):
    """
    There are four kinds of spiders: common, ajax, gfw, ajax_gfw. If you don't assign any tasks, all these spiders will run.
    """
    if not tasks:
        spiders = all_spiders
    else:
        spiders = list()
        for task in tasks:
            for spider in all_spiders:
                if spider.name == task:
                    spiders.append(spider)
                    break
    logger.info(f"{len(spiders)} spiders will starts up")
    if not spiders:
        return
    settings = get_project_settings()
    runner = CrawlerRunner(settings)
    for spider in spiders:
        runner.crawl(spider)
    d = runner.join()
    d.addBoth(lambda _: reactor.stop())
    reactor.run()
