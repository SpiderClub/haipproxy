"""
Useful mixin class for all the spiders.
"""


class BaseSpider:
    # slow down each spider
    custom_settings = {
        'CONCURRENT_REQUESTS_PER_DOMAIN': 1,
        'DOWNLOAD_DELAY': 3
    }

    def procotol_extractor(self, detail):
        # TODO it might be socks4, fix this case
        if 'socks' in detail:
            protocols = ['socks5']
        # TODO find a better way to recongnize both http and https protocol
        elif 'http,https' in detail:
            protocols = ['http', 'https']
        elif 'https' in detail:
            protocols = ['https']
        else:
            protocols = ['http']

        return protocols

    def construct_proxy_url(self, scheme, ip, port):
        return '{}://{}:{}'.format(scheme, ip, port)



