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

    def parse(self, response):
        url = response.url
        if self.exists(url, 'proxy-list'):
            items = self.parse_common(response, pre_extract_method='css', pre_extract='.table ul',
                                      detail_rule='li::text', split_detail=True)
        elif self.exists(url, 'cnproxy'):
            items = self.parse_cnproxy(response)
        elif self.exists(url, 'free-proxy'):
            items = self.parse_free_proxy(response)
        elif self.exists(url, 'proxylist'):
            items = self.parse_proxylist(response)
        else:
            items = self.parse_common(response)

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

    def parse_proxylist(self, response):
        items = list()
        infos = response.xpath('//tr')[2:]

        for info in infos:
            info_str = info.extract()
            if '透明' in info_str or 'transparent' in info_str.lower():
                continue
            ip = info.css('td::text')[1].extract()
            port = info.css('td a::text')[0].extract()
            if not ip or not port:
                continue

            cur_protocols = self.procotol_extractor(info_str)
            for protocol in cur_protocols:
                items.append(ProxyUrlItem(url=self.construct_proxy_url(protocol, ip, port)))

            return items
