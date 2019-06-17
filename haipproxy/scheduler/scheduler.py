"""
This module schedules all the tasks according to config.rules.
"""
import time
from multiprocessing import Pool

import click
import schedule
from twisted.internet import reactor
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings

from ..client import SquidClient
# from logger import (
#     crawler_logger, scheduler_logger,
#     client_logger)
from ..config.rules import (CRAWLER_TASKS, VALIDATOR_TASKS, CRAWLER_TASK_MAPS,
                            TEMP_TASK_MAPS)
from ..crawler.spiders import all_spiders
from ..crawler.validators import all_validators
from ..config.settings import (SPIDER_COMMON_TASK, SPIDER_AJAX_TASK,
                               SPIDER_GFW_TASK, SPIDER_AJAX_GFW_TASK,
                               TEMP_HTTP_QUEUE, TEMP_HTTPS_QUEUE,
                               TIMER_RECORDER, TTL_VALIDATED_RESOURCE)
from ..utils import (get_redis_conn, acquire_lock, release_lock)

DEFAULT_CRAWLER_TASKS = [
    SPIDER_COMMON_TASK, SPIDER_AJAX_TASK, SPIDER_GFW_TASK, SPIDER_AJAX_GFW_TASK
]
DEFAULT_VALIDATORS_TASKS = [TEMP_HTTP_QUEUE, TEMP_HTTPS_QUEUE]

DEFAULT_CRAWLERS = all_spiders
DEFAULT_VALIDATORS = all_validators


class BaseCase:
    def __init__(self, spider):
        self.spider = spider

    def check(self, task, maps):
        task_queue = maps.get(task)
        return self.spider.task_queue == task_queue


class BaseScheduler:
    def __init__(self, name, tasks, task_queues=None):
        """
        init function for schedulers.
        :param name: scheduler name, generally the value is used by the scheduler
        :param tasks: tasks in config.rules
        :param task_queues: for crawler, the value is task_queue, while for validator, it's task name
        """
        self.name = name
        self.tasks = tasks
        self.task_queues = list() if not task_queues else task_queues

    def schedule_with_delay(self):
        for task in self.tasks:
            interval = task.get('interval')
            schedule.every(interval).minutes.do(self.schedule_task_with_lock,
                                                task)
        while True:
            schedule.run_pending()
            time.sleep(1)

    def schedule_all_right_now(self):
        with Pool() as pool:
            pool.map(self.schedule_task_with_lock, self.tasks)

    def get_lock(self, conn, task):
        if not task.get('enable'):
            return None
        task_queue = task.get('task_queue')
        if task_queue not in self.task_queues:
            return None

        task_name = task.get('name')
        lock_indentifier = acquire_lock(conn, task_name)
        return lock_indentifier

    def schedule_task_with_lock(self, task):
        raise NotImplementedError


class CrawlerScheduler(BaseScheduler):
    def schedule_task_with_lock(self, task):
        """Crawler scheduler filters tasks according to task type"""
        if not task.get('enable'):
            return None
        task_queue = task.get('task_queue')
        if task_queue not in self.task_queues:
            return None

        conn = get_redis_conn()
        task_name = task.get('name')
        interval = task.get('interval')
        urls = task.get('resource')
        lock_indentifier = acquire_lock(conn, task_name)
        if not lock_indentifier:
            return False

        pipe = conn.pipeline(True)
        try:
            now = int(time.time())
            pipe.hget(TIMER_RECORDER, task_name)
            r = pipe.execute()[0]
            if not r or (now - int(r.decode('utf-8'))) >= interval * 60:
                pipe.lpush(task_queue, *urls)
                pipe.hset(TIMER_RECORDER, task_name, now)
                pipe.execute()
                # scheduler_logger.info('crawler task {} has been stored into redis successfully'.format(task_name))
                return True
            else:
                return None
        finally:
            release_lock(conn, task_name, lock_indentifier)


class ValidatorScheduler(BaseScheduler):
    def schedule_task_with_lock(self, task):
        """Validator scheduler filters tasks according to task name
        since its task name stands for task type"""
        if not task.get('enable'):
            return None
        task_queue = task.get('task_queue')
        if task_queue not in self.task_queues:
            return None

        conn = get_redis_conn()
        interval = task.get('interval')
        task_name = task.get('name')
        resource_queue = task.get('resource')
        lock_indentifier = acquire_lock(conn, task_name)
        if not lock_indentifier:
            return False
        pipe = conn.pipeline(True)
        try:
            now = int(time.time())
            pipe.hget(TIMER_RECORDER, task_name)
            pipe.zrevrangebyscore(resource_queue, '+inf', '-inf')
            r, proxies = pipe.execute()
            if not r or (now - int(r.decode('utf-8'))) >= interval * 60:
                if not proxies:
                    # scheduler_logger.warning('fetched no proxies from task {}'.format(task_name))
                    print('fetched no proxies from task {}'.format(task_name))
                    return None

                pipe.sadd(task_queue, *proxies)
                pipe.hset(TIMER_RECORDER, task_name, now)
                pipe.execute()
                # scheduler_logger.info('validator task {} has been stored into redis successfully'.format(task_name))
                return True
            else:
                return None
        finally:
            release_lock(conn, task_name, lock_indentifier)


@click.command()
@click.option('--usage',
              type=click.Choice(['crawler', 'validator']),
              default='crawler')
@click.argument('task_queues', nargs=-1)
def scheduler_start(usage, task_queues):
    """Start specified scheduler."""
    # scheduler_logger.info('{} scheduler is starting...'.format(usage))
    print('{} scheduler is starting...'.format(usage))
    if usage == 'crawler':
        default_tasks = CRAWLER_TASKS
        default_allow_tasks = DEFAULT_CRAWLER_TASKS
        maps = CRAWLER_TASK_MAPS
        SchedulerCls = CrawlerScheduler
    else:
        default_tasks = VALIDATOR_TASKS
        default_allow_tasks = DEFAULT_VALIDATORS_TASKS
        maps = TEMP_TASK_MAPS
        SchedulerCls = ValidatorScheduler

    scheduler = SchedulerCls(usage, default_tasks)

    if not task_queues:
        scheduler.task_queues = default_allow_tasks
    else:
        for task_queue in task_queues:
            allow_task_queue = maps.get(task_queue)
            if not allow_task_queue:
                # scheduler_logger.warning('scheduler task {} is an invalid task, the allowed tasks are {}'.format(
                #     task_queue, list(maps.keys())))
                print(
                    'scheduler task {} is an invalid task, the allowed tasks are {}'
                    .format(task_queue, list(maps.keys())))
                continue
            scheduler.task_queues.append(allow_task_queue)

    scheduler.schedule_all_right_now()
    scheduler.schedule_with_delay()


@click.command()
@click.option('--usage',
              type=click.Choice(['crawler', 'validator']),
              default='crawler')
@click.argument('tasks', nargs=-1)
def crawler_start(usage, tasks):
    """Start specified spiders or validators from cmd with scrapy core api.
    There are four kinds of spiders: common, ajax, gfw, ajax_gfw. If you don't
    assign any tasks, all these spiders will run.
    """
    if usage == 'crawler':
        maps = CRAWLER_TASK_MAPS
        origin_spiders = DEFAULT_CRAWLERS
    else:
        maps = TEMP_TASK_MAPS
        origin_spiders = DEFAULT_VALIDATORS

    if not tasks:
        spiders = origin_spiders
    else:
        spiders = list()
        cases = list(map(BaseCase, origin_spiders))
        for task in tasks:
            for case in cases:
                if case.check(task, maps):
                    spiders.append(case.spider)
                    break
            else:
                # crawler_logger.warning('spider task {} is an invalid task, the allowed tasks are {}'.format(
                #     task, list(maps.keys())))
                pass
    if not spiders:
        #crawler_logger.warning('no spider starts up, please check your task input')
        return

    settings = get_project_settings()
    configure_logging(settings)
    runner = CrawlerRunner(settings)
    for spider in spiders:
        runner.crawl(spider)
    d = runner.join()
    d.addBoth(lambda _: reactor.stop())
    reactor.run()


@click.command()
@click.option('--usage', default='https', help='Usage of squid')
@click.option('--interval',
              default=TTL_VALIDATED_RESOURCE,
              help='Updating frenquency of squid conf.')
def squid_conf_update(usage, interval):
    """Timertask for updating proxies for squid config file"""
    # client_logger.info('the updating task is starting...')
    client = SquidClient(usage)
    client.update_conf()
    schedule.every(interval).minutes.do(client.update_conf)
    while True:
        schedule.run_pending()
        time.sleep(1)
