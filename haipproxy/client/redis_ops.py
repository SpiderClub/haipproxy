import logging
import time

from haipproxy.utils import get_redis_conn

logger = logging.getLogger(__name__)


class ProxyMaintainer:
    def __init__(self):
        self.redis_conn = get_redis_conn()
        self.rpipe = self.redis_conn.pipeline()

    def del_all_fails(self):
        total = 0
        nfail = 0
        for pkey in self.redis_conn.scan_iter(match='*://*'):
            total += 1
            if self.redis_conn.hget(pkey, 'used_count') != b'0' and \
                self.redis_conn.hget(pkey, 'success_count') == b'0':
                self.rpipe.delete(pkey)
                nfail += 1
        self.rpipe.execute()
        logger.info(
            f'{nfail} failed proxies deleted, {total} before, {total - nfail} now '
        )
