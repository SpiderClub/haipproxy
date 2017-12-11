"""
haipproxy parser's rules.
~~~~~~~~~~~~~~

Schduler will parse response text according to the rules.
"""

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
        'enable': True
    }
]