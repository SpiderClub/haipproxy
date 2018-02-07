import click
from twisted.internet import reactor
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings


class BaseCase:
    def __init__(self, spider):
        self.spider = spider

    def check(self, name):
        return self.spider.name == name


class SpiderBootstrap:
    @staticmethod
    @click.command()
    @click.argument('names', nargs=-1)
    def start(names, origin_spiders):
        """start specified spiders from cmd with scrapy core api"""
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