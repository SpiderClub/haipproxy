"""
Useful base class for all spiders.
"""
import json
import ipaddress

from haipproxy.config.rules import CRAWLER_TASKS
from ..items import ProxyUrlItem


class BaseSpider:
    default_protocols = ['http']
    # slow down each spider
    custom_settings = {
        'CONCURRENT_REQUESTS_PER_DOMAIN': 5,
        'DOWNLOAD_DELAY': 3,
        'EXTENSIONS': {
            'haipproxy.crawler.extensions.FailLogger': 500,
        },
        'DOWNLOADER_MIDDLEWARES': {
            'haipproxy.crawler.middlewares.ErrorTraceMiddleware': 200,
        },
        'ITEM_PIPELINES': {
            'haipproxy.crawler.pipelines.ProxyIPPipeline': 200,
        }
    }

    def __init__(self):
        self.parser_maps = {
            'common': self.parse_common,
            'json': self.parse_json,
            'text': self.parse_raw_text,
        }

    def parse(self, response):
        url = response.url
        items = list()
        for task in CRAWLER_TASKS:
            if self.exists(url, task['name']):
                parse_type = task['parse_type']
                func = self.parser_maps.get(parse_type)
                parse_rule = task.get('parse_rule')
                if parse_rule:
                    items = func(response, **parse_rule)
                else:
                    items = func(response)

        for item in items:
            yield item

    def parse_common(self,
                     response,
                     pre_extract_method='xpath',
                     pre_extract='//tr',
                     infos_pos=1,
                     infos_end=None,
                     detail_rule='td::text',
                     ip_pos=0,
                     port_pos=1,
                     extract_protocol=True,
                     split_detail=False,
                     protocols=None):
        """
        Common response parser
        :param response: scrapy response
        :param pre_extract_method: extracting method for extracting all infos, xpath is the default value
        :param pre_extract: pre parsing rule for extracing all infos
        :param infos_pos: pos for extracting infos
        :param infos_end: end pos for extracting infos, its value should be smaller than 0
        :param detail_rule: rule for extracting ip and port block, css selector is used here
        :param ip_pos: ip index
        :param port_pos: port index
        :param extract_protocol: if extract_protocol == False, default protocols will be used
        :param split_detail: if split_detail == True, ':' will be used to split ip:port
        :param protocols: this value will be used for the ip's protocols
        :return: ip infos
        """
        if pre_extract_method == 'xpath':
            infos = response.xpath(pre_extract)[infos_pos:infos_end]
        else:
            infos = response.css(pre_extract)
        items = list()
        for info in infos:
            info_str = info.extract()
            if '透明' in info_str or 'transparent' in info_str.lower():
                continue
            proxy_detail = info.css(detail_rule).extract()
            if not proxy_detail:
                continue

            if not split_detail:
                ip = proxy_detail[ip_pos].strip()
                port = proxy_detail[port_pos].strip()
            else:
                ip, port = proxy_detail[0].split(':')
            if not self.proxy_check(ip, port):
                continue

            if protocols:
                cur_protocols = protocols
            elif extract_protocol:
                cur_protocols = self.procotol_extractor(info_str)
            else:
                cur_protocols = self.default_protocols

            for protocol in cur_protocols:
                items.append(
                    ProxyUrlItem(
                        url=self.construct_proxy_url(protocol, ip, port)))

        return items

    def parse_json(self, response, detail_rule, ip_key='ip', port_key='port'):
        """
        Json response parser
        :param response: scrapy response
        :param detail_rule: json parser rules, its type is list
        :param ip_key: ip extractor
        :param port_key: port extractor
        :return: ip infos
        """
        infos = json.loads(response.body.decode('utf-8'))
        items = list()

        for r in detail_rule:
            infos = infos.get(r)
        for info in infos:
            ip = info.get(ip_key)
            port = info.get(port_key)
            if not self.proxy_check(ip, port):
                continue

            protocols = self.procotol_extractor(str(info))
            for protocol in protocols:
                items.append(
                    ProxyUrlItem(
                        url=self.construct_proxy_url(protocol, ip, port)))

        return items

    def parse_raw_text(self,
                       response,
                       pre_extract=None,
                       delimiter='\r\n',
                       redundancy=None,
                       protocols=None):
        """
        Raw response parser
        :param response: scrapy response
        :param pre_extract: pre parsing rule for extracing all infos, css selector is used here
        :param delimiter: split ip and port info from response
        :param redundancy: remove redundancy from ip info
        :param protocols: default procotols
        :return: ip infos
        """
        items = list()
        if pre_extract:
            infos = response.css(pre_extract).extract()
        else:
            infos = response.text.split(delimiter)
        for info in infos:
            if ':' not in info:
                continue
            if redundancy:
                info = info[:info.find(redundancy)]

            ip, port = info.split(':')
            if not ip or not port:
                continue

            if not self.proxy_check(ip, port):
                continue

            protocols = self.default_protocols if not protocols else protocols

            for protocol in protocols:
                items.append(
                    ProxyUrlItem(
                        url=self.construct_proxy_url(protocol, ip, port)))
        return items

    def procotol_extractor(self, detail):
        """extract http protocol,default value is http"""
        detail = detail.lower()
        if 'socks5' in detail:
            protocols = ['socks5']
        elif 'socks4/5' in detail:
            protocols = ['socks4', 'socks5']
        elif 'socks4' in detail:
            protocols = ['socks4']
        else:
            protocols = self.default_protocols
        return protocols

    def proxy_check(self, ip, port):
        """
        check whether the proxy ip and port are valid
        :param ip: proxy ip value
        :param port: proxy port value
        :return: True or False
        """
        try:
            ipaddress.ip_address(ip)
            p = int(port)
            if p > 65535 or p <= 0:
                return False
        except ValueError:
            return False
        return True

    def construct_proxy_url(self, scheme, ip, port):
        """construct proxy urls, so spiders can use them directly"""
        return '{}://{}:{}'.format(scheme, ip, port)

    def exists(self, url, *flags):
        """check whether the flag of the url is set or not"""
        for flag in flags:
            if flag in url:
                return True
        return False
