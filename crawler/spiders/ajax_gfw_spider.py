"""
Ajax gfw proxy ip crawler with scrapy-splash
"""
from config.settings import SPIDER_AJAX_GFW_TASK
from ..redis_spiders import RedisAjaxSpider
from ..items import ProxyUrlItem
from .mixin import BaseSpider


class AjaxGFWSpider(BaseSpider, RedisAjaxSpider):
    name = 'ajax_gfw'
    proxy_mode = 2
    task_type = SPIDER_AJAX_GFW_TASK

    def parse(self, response):
        if 'proxy-list' in response.url:
            items = self.parse_common(response, pre_extract_method='css', pre_extract='.table ul',
                                      detail_rule='li::text', split_detail=True)
        elif 'cnproxy' in response.url:
            items = self.parse_cnproxy(response)
        elif 'free-proxy' in response.url:
            items = self.parse_free_proxy(response)
        else:
            items = list()

        for item in items:
            yield item

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






