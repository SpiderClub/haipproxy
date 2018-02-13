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

from client import SquidClient
from config.rules import (
    CRWALER_TASKS, VALIDATOR_TASKS,
    CRAWLER_TASK_MAPS, VALIDATOR_TASK_MAPS)
from crawler.spiders import (
    CommonSpider, AjaxSpider,
    GFWSpider, AjaxGFWSpider)
from crawler.validators import (
    HttpBinInitValidator, CommonValidator)
from config.settings import (
    SPIDER_COMMON_TASK, SPIDER_AJAX_TASK,
    SPIDER_GFW_TASK, SPIDER_AJAX_GFW_TASK,
    VALIDATOR_HTTP_TASK, VALIDATOR_HTTPS_TASK,
    TIMER_RECORDER, SQUID_UPDATE_INTERNAL)
from utils.redis_util import (
    get_redis_conn, acquire_lock,
    release_lock)


DEFAULT_CRAWLER_TASKS = [
    SPIDER_COMMON_TASK, SPIDER_AJAX_TASK,
    SPIDER_GFW_TASK, SPIDER_AJAX_GFW_TASK]
DEFAULT_VALIDATORS_TASKS = [VALIDATOR_HTTP_TASK, VALIDATOR_HTTPS_TASK]

DEFAULT_CRAWLERS = [CommonSpider, AjaxSpider, GFWSpider, AjaxGFWSpider]
DEFAULT_VALIDATORS = [HttpBinInitValidator, CommonValidator]


class BaseCase:
    def __init__(self, spider):
        self.spider = spider

    def check(self, task):
        if hasattr(self.spider, 'task_type'):
            task_type = CRAWLER_TASK_MAPS.get(task)
            return self.spider.task_type == task_type
        print(task)
        print(self.spider.name)
        print(self.spider.name == task)
        return self.spider.name == task


class BaseScheduler:
    def __init__(self, name, tasks, task_types=None):
        """
        init function for schedulers.
        :param name: scheduler name, generally the value is usage of the scheduler
        :param tasks: tasks in config.rules
        :param task_types: for crawler, the value is task_type,while for validator, it's task name
        """
        self.name = name
        self.tasks = tasks
        self.task_types = list() if not task_types else task_types

    def schedule_with_delay(self):
        for task in self.tasks:
            internal = task.get('internal')
            schedule.every(internal).minutes.do(self.schedule_task_with_lock, task)
        while True:
            schedule.run_pending()
            time.sleep(1)

    def schedule_all_right_now(self):
        with Pool() as pool:
            pool.map(self.schedule_task_with_lock, self.tasks)

    def get_lock(self, conn, task):
        if not task.get('enable'):
            return None
        task_type = task.get('task_type')
        if task_type not in self.task_types:
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
        task_type = task.get('task_type')
        if task_type not in self.task_types:
            return None

        conn = get_redis_conn()
        task_name = task.get('name')
        internal = task.get('internal')
        urls = task.get('resource')
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
                print('crawler task {} has been stored into redis successfully'.format(task_name))
                return True
            else:
                return None
        finally:
            release_lock(conn, task_name, lock_indentifier)


class ValidatorScheduler(BaseScheduler):
    def schedule_task_with_lock(self, task):
        """Validator scheduler filters tasks according to task name
        since it's task name stands for task type"""
        if not task.get('enable'):
            return None
        task_type = task.get('task_type')
        if task_type not in self.task_types:
            return None

        conn = get_redis_conn()
        internal = task.get('internal')
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
            if not r or (now - int(r.decode('utf-8'))) >= internal * 60:
                if not proxies:
                    print('fetched no proxies from task {}'.format(task_name))
                    return None

                pipe.rpush(task_type, *proxies)
                pipe.hset(TIMER_RECORDER, task_name, now)
                pipe.execute()
                print('validator task {} has been stored into redis successfully'.format(task_name))
                return True
            else:
                return None
        finally:
            release_lock(conn, task_name, lock_indentifier)


@click.command()
@click.option('--usage', type=click.Choice(['crawler', 'validator']), default='crawler')
@click.argument('task_types', nargs=-1)
def scheduler_start(usage, task_types):
    """Start specified scheduler."""
    default_tasks = CRWALER_TASKS if usage == 'crawler' else VALIDATOR_TASKS
    default_allow_tasks = DEFAULT_CRAWLER_TASKS if usage == 'crawler' else DEFAULT_VALIDATORS_TASKS
    maps = CRAWLER_TASK_MAPS if usage == 'crawler' else VALIDATOR_TASK_MAPS
    SchedulerCls = CrawlerScheduler if usage == 'crawler' else ValidatorScheduler
    scheduler = SchedulerCls(usage, default_tasks)

    if not task_types:
        scheduler.task_types = default_allow_tasks
    else:
        for task_type in task_types:
            allow_task_type = maps.get(task_type)
            if not allow_task_type:
                continue
            scheduler.task_types.append(allow_task_type)

    scheduler.schedule_all_right_now()
    scheduler.schedule_with_delay()


@click.command()
@click.option('--usage', type=click.Choice(['crawler', 'validator']), default='crawler')
@click.argument('tasks', nargs=-1)
def crawler_start(usage, tasks):
    """Start specified spiders or validators from cmd with scrapy core api.
    There are four kinds of spiders: common, ajax, gfw, ajax_gfw.If you don't
    assign any tasks, all the spiders will run.
    """
    origin_spiders = DEFAULT_CRAWLERS if usage == 'crawler' else DEFAULT_VALIDATORS
    if not tasks:
        spiders = origin_spiders
    else:
        spiders = list()
        cases = list(map(BaseCase, origin_spiders))
        for task in tasks:
            for case in cases:
                if case.check(task):
                    spiders.append(case.spider)

    settings = get_project_settings()
    configure_logging(settings)
    runner = CrawlerRunner(settings)
    for spider in spiders:
        runner.crawl(spider)
    d = runner.join()
    d.addBoth(lambda _: reactor.stop())
    reactor.run()


@click.command()
@click.option('--internal', default=SQUID_UPDATE_INTERNAL, help='Updating frenquency of squid conf.')
def squid_conf_update(internal):
    """Timertask for updating proxies for squid config file"""
    print('the updating task is starting...')
    client = SquidClient('https')
    schedule.every(internal).minutes.do(client.update_conf)
    while True:
        schedule.run_pending()
        time.sleep(1)