"""
Ajax gfw proxy ip crawler with scrapy-splash
"""
from config.settings import SPIDER_AJAX_GFW_TASK
from ..redis_spiders import RedisAjaxSpider
from ..items import ProxyUrlItem
from .base import BaseSpider


class AjaxGFWSpider(BaseSpider, RedisAjaxSpider):
    name = 'ajax_gfw'
    proxy_mode = 2
    task_queue = SPIDER_AJAX_GFW_TASK

    def __init__(self):
        super().__init__()
        self.parser_maps.setdefault('cnproxy', self.parse_cnproxy)
        self.parser_maps.setdefault('free-proxy', self.parse_free_proxy)

    def parse_cnproxy(self, response):
        items = list()
        infos = response.xpath('//tr')[2:]
        for info in infos:
            info_str = info.extract()
            proxy_detail = info.css('td::text').extract()
            ip = proxy_detail[0].strip()
            port = proxy_detail[1][1:].strip()
            cur_protocols = self.procotol_extractor(info_str)
            for protocol in cur_protocols:
                items.append(ProxyUrlItem(url=self.construct_proxy_url(protocol, ip, port)))

        return items

    def parse_free_proxy(self, response):
        items = list()
        infos = response.xpath('//table[@id="proxy_list"]').css('tr')[1:]
        for info in infos:
            info_str = info.extract()
            ip = info.css('abbr::text').extract_first()
            port = info.css('.fport::text').extract_first()
            if not ip or not port:
                continue

            cur_protocols = self.procotol_extractor(info_str)
            for protocol in cur_protocols:
                items.append(ProxyUrlItem(url=self.construct_proxy_url(protocol, ip, port)))

        return items


