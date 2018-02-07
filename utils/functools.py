import click
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
from scheduler import (
    CrawlerScheduler, ValidatorScheduler)
from config.settings import (
    SPIDER_COMMON_TASK, SPIDER_AJAX_TASK,
    SPIDER_GFW_TASK, SPIDER_AJAX_GFW_TASK,
    HTTP_QUEUE, VALIDATOR_HTTP_TASK,
    VALIDATOR_HTTPS_TASK)


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
