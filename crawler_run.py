"""
This module is used to start multi spiders from ide or cmd.
"""
import click
from twisted.internet import reactor
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings

from crawler.spiders import (
    CommonSpider, AjaxSpider, GFWSpider, AjaxGFWSpider)


ALL_SPIDERS = [CommonSpider, AjaxSpider, GFWSpider, AjaxGFWSpider]


class BaseCase:
    def __init__(self, spider):
        self.spider = spider

    def check(self, name):
        return self.spider.name == name


@click.command()
@click.argument('names', nargs=-1)
def start(names):
    """start specified spiders from cmd with scrapy core api"""
    spiders = list()
    all_cases = [BaseCase(CommonSpider), BaseCase(AjaxSpider)]
    if not names:
        spiders = ALL_SPIDERS
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


if __name__ == '__main__':
    start()
