"""
Useful mixin class for all the spiders.
"""
import json

from ..items import ProxyUrlItem


class BaseSpider:
    default_protocols = ['http', 'https']
    # slow down each spider
    custom_settings = {
        'CONCURRENT_REQUESTS_PER_DOMAIN': 1,
        'DOWNLOAD_DELAY': 3
    }

    def parse_common(self, response, pre_extract='//tr', infos_pos=1,
                     detail_rule='td::text', ip_pos=0, port_pos=1, extract_protocol=True):
        """
        Common response parser
        :param response: scrapy response
        :param pre_extract: pre parsing rule for extracing all infos
        :param infos_pos: pos for extracting infos
        :param detail_rule: rule for extracting ip and port block
        :param ip_pos: ip index
        :param port_pos: port index
        :param extract_protocol: if extract_protocol == False, default protocols will be used
        :return: ip infos
        """
        infos = response.xpath(pre_extract)[infos_pos:]
        items = list()

        for info in infos:
            info_str = info.extract()
            if 'ip' in info_str or '透明' in info_str:
                continue

            proxy_detail = info.css(detail_rule).extract()
            if not proxy_detail:
                continue

            ip = proxy_detail[ip_pos].strip()
            port = proxy_detail[port_pos].strip()
            if extract_protocol:
                protocols = self.procotol_extractor(info_str)
            else:
                protocols = self.default_protocols

            for protocol in protocols:
                items.append(ProxyUrlItem(url=self.construct_proxy_url(protocol, ip, port)))

        return items

    def parse_json(self, response, detail_rule, ip_key='ip', port_key='port'):
        """
        Json response parser
        :param response: scrapy response
        :param detail_rule: json parser rules, its type is list
        :param ip_key: ip extractor
        :param port_key: port extrator
        :return: ip infos
        """
        infos = json.loads(response.body.decode('utf-8'))
        items = list()

        for r in detail_rule:
            infos = infos.get(r)
        for info in infos:
            ip = info.get(ip_key)
            port = info.get(port_key)
            protocols = self.procotol_extractor(str(info))
            for protocol in protocols:
                items.append(ProxyUrlItem(url=self.construct_proxy_url(protocol, ip, port)))

        return items

    def procotol_extractor(self, detail):
        """extract http protocol,default value is http and https"""
        detail = detail.lower()
        # TODO it might be socks4, fix this case
        if 'socks' in detail:
            protocols = ['socks5']
        # TODO find a better way to recongnize both http and https protocol
        elif 'http,https' in detail or 'http/https' in detail:
            protocols = ['http', 'https']
        elif 'https' in detail:
            protocols = ['https']
        elif 'http' in detail:
            protocols = ['http']
        else:
            protocols = ['http', 'https']
        return protocols

    def construct_proxy_url(self, scheme, ip, port):
        """construct proxy urls so spiders can directly use them"""
        return '{}://{}:{}'.format(scheme, ip, port)



