import time

from prometheus_client import start_http_server
from prometheus_client.core import (CounterMetricFamily, REGISTRY)
from haipproxy.utils import get_redis_conn

from examples.zhihu.configs import TOTAL_SUCCESS_REQUESTS


class CustomCollector:
    def __init__(self):
        self.redis_conn = get_redis_conn()

    def collect(self):
        try:
            redis_count = int(
                self.redis_conn.get(TOTAL_SUCCESS_REQUESTS).decode())
        except AttributeError:
            redis_count = 0
        yield CounterMetricFamily('total_success_requests',
                                  'successful requests',
                                  value=redis_count)


if __name__ == '__main__':
    port = 7000
    print('starting server http://127.0.0.1:{}/metrics'.format(port))
    REGISTRY.register(CustomCollector())
    start_http_server(port, addr='0.0.0.0')
    while True:
        time.sleep(3)
