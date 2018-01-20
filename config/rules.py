"""
haipproxy parser's rules.
Schduler will parse response text according to the rules.
"""


# todo: consider incremental crawling and incremental parser
# todo: consider filter transport ip
# todo: consider use socks5 to crawl the website outsite the wall
parser_rules = [
    {
        'name': 'xici',
        'url_list': ['http://www.xicidaili.com/nn/{}'.format(i) for i in range(1, 11)],
        'parser_method': 'bs',
        'paser_pattern': {
            'ip': '',
            'port': '',
            'type': ''
        },
        'need_proxy': False,
        'need_increment': True,
        'enable': True
    },
    {
        'name': 'kuaidaili',
        'url_list': ['http://www.kuaidaili.com/free/inha/{}'.format(i) for i in range(1, 11)],
        'parser_method': 'bs',
        'parser_pattern': {
            'ip': '',
            'port': '',
            'type': ''
        },
        'need_proxy': False,
        'need_increment': True,
        'enable': True
    }
]