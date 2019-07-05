import logging
import time

from prometheus_client import start_http_server
from prometheus_client.core import (CounterMetricFamily, GaugeMetricFamily,
                                    REGISTRY)

from haipproxy.config.settings import (
    DATA_ALL,
    EXPORTER_LISTEN_HOST,
    EXPORTER_LISTEN_PORT,
)
from haipproxy.utils import get_redis_conn

logger = logging.getLogger(__name__)


class CustomCollector:
    def __init__(self):
        self.redis_conn = get_redis_conn()

    def collect(self):
        start_time = int(time.time()) - 2 * 60

        pipe = self.redis_conn.pipeline(False)
        pipe.scard(DATA_ALL)
        r = pipe.execute()

        yield CounterMetricFamily('total_proxies', 'total proxies', r[0])
        # yield GaugeMetricFamily('init_proxies', 'total init proxies', r[1])


def exporter_start():
    logger.info('starting server http://{}:{}/metrics'.format(
        EXPORTER_LISTEN_HOST, EXPORTER_LISTEN_PORT))
    REGISTRY.register(CustomCollector())
    start_http_server(EXPORTER_LISTEN_PORT, addr=EXPORTER_LISTEN_HOST)
    while True:
        time.sleep(5)
