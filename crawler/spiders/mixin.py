"""
Useful mixin class for all the spiders.
"""


class IPSourceMixin:
    def construct_proxy_url(self, scheme, ip, port):
        return '{}://{}:{}'.format(scheme, ip, port)