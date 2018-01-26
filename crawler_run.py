"""
This module is used to start multi spiders from ide or cmd.
"""
from twisted.internet import reactor
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings

from crawler.spiders import (
    CommonSpider, AjaxSpider, CrawlSpider, GFWSpider, AjaxGFWSpider)


all_spiders = [
    CommonSpider, AjaxSpider, CrawlSpider, GFWSpider, AjaxGFWSpider
]


def start():
    """start all spiders from scrapy core api"""
    settings = get_project_settings()
    configure_logging(settings)
    runner = CrawlerRunner(settings)
    for spider in all_spiders:
        runner.crawl(spider)
    d = runner.join()
    d.addBoth(lambda _: reactor.stop())
    reactor.run()


if __name__ == '__main__':
    start()
