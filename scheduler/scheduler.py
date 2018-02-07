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

from config.rules import (
    CRWALER_TASKS, VALIDATOR_TASKS)
from crawler.spiders import (
    CommonSpider, AjaxSpider,
    GFWSpider, AjaxGFWSpider)
from crawler.validators import (
    HttpBinInitValidator, CommonValidator)
from config.settings import (
    SPIDER_COMMON_TASK, SPIDER_AJAX_TASK,
    SPIDER_GFW_TASK, SPIDER_AJAX_GFW_TASK,
    HTTP_QUEUE, VALIDATOR_HTTP_TASK,
    VALIDATOR_HTTPS_TASK, TIMER_RECORDER)
from utils.redis_util import (
    get_redis_con, acquire_lock,
    release_lock)


DEFAULT_CRAWLER_TASKS = [
    SPIDER_COMMON_TASK, SPIDER_AJAX_TASK,
    SPIDER_GFW_TASK, SPIDER_AJAX_GFW_TASK]
DEFAULT_VALIDATORS_TASKS = [HTTP_QUEUE, VALIDATOR_HTTP_TASK,
                            VALIDATOR_HTTPS_TASK]

PROXY_CRAWLERS = [CommonSpider, AjaxSpider, GFWSpider, AjaxGFWSpider]
PROXY_VALIDATORS = [HttpBinInitValidator, CommonValidator]


class BaseCase:
    def __init__(self, spider):
        self.spider = spider

    def check(self, name):
        return self.spider.name == name


class BaseScheduler:
    def __init__(self, name, tasks):
        self.name = name
        self.tasks = tasks
        self.allow_tasks = list()

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

    def schedule_task_with_lock(self, task):
        if not task.get('enable'):
            return None


class CrawlerScheduler(BaseScheduler):
    def schedule_task_with_lock(self, task):
        """Crawler scheduler filters tasks according to task type"""
        if not task.get('enable'):
            return None
        task_type = task.get('task_type')

        if task_type not in self.allow_tasks:
            return None

        conn = get_redis_con()
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
        since it's task name can stand for task type"""
        if not task.get('enable'):
            return None

        task_name = task.get('name')
        if task_name not in self.allow_tasks:
            return None

        conn = get_redis_con()
        internal = task.get('internal')
        task_type = task.get('task_type')
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
@click.argument('names', nargs=-1)
def crawler_start(usage, names):
    """start specified spiders or validators from cmd with scrapy core api"""
    if usage == 'crawler':
        origin_spiders = PROXY_CRAWLERS
    else:
        origin_spiders = PROXY_VALIDATORS

    spiders = list()
    all_cases = list(map(BaseCase, origin_spiders))
    if not names:
        spiders = origin_spiders
    else:
        for spider_name in names:
            for case in all_cases:
                if case.check(spider_name):
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
@click.option('--usage', type=click.Choice(['crawler', 'validator']), default='crawler')
@click.argument('tasks', nargs=-1)
def scheduler_start(usage, tasks):
    """start specified scheduler"""
    if usage == 'crawler':
        scheduler = CrawlerScheduler(usage, CRWALER_TASKS)
        if not tasks:
            scheduler.allow_tasks = DEFAULT_CRAWLER_TASKS
        else:
            pass
    else:
        scheduler = ValidatorScheduler(usage, VALIDATOR_TASKS)
        if not tasks:
            scheduler.allow_tasks = DEFAULT_VALIDATORS_TASKS

    scheduler.schedule_all_right_now()
    scheduler.schedule_with_delay()
