import heapq
import logging
import math
import threading
import time

from haipproxy.utils import get_redis_conn

logger = logging.getLogger(__name__)


class ProxyClient(object):
    def __init__(self):
        self.redis_conn = get_redis_conn()
        self.rpipe = self.redis_conn.pipeline()
        self.pheap = []
        self._fill_pool()
        self.idx = -1
        # t = threading.Thread(target=self._refresh_periodically)
        # t.setDaemon(True)
        # t.start()

    def del_all_fails(self):
        total = 0
        nfail = 0
        for pkey in self.redis_conn.scan_iter(match='*://*'):
            total += 1
            used_count, success_count = self.redis_conn.hmget(
                pkey, 'used_count', 'success_count')
            if used_count > b'1' and success_count == '0':
                self.rpipe.delete(pkey)
                nfail += 1
        self.rpipe.execute()
        logger.info(
            f'{nfail} failed proxies deleted, {total} before, {total - nfail} now '
        )

    def next_proxy(self, protocol=''):
        self.protocol = protocol.lower()
        if self.protocol != '':
            self.protocol += ':'

        while 1:
            self.idx = self.idx + 1
            if self.idx >= len(self.pheap):
                self.idx = -1
                raise StopIteration
            if self.pheap[self.idx][1].startswith(self.protocol):
                yield self.pheap[self.idx][1]

    def _refresh_periodically(self):
        while True:
            # lock
            self.pheap.clear()
            self._fill_pool()
            time.sleep(3600)

    def _fill_pool(self):
        total = 0
        for pkey in self.redis_conn.scan_iter(match='*://*'):
            total += 1
            stat = self.redis_conn.hgetall(pkey)
            score = self.cal_score(stat)
            self.redis_conn.hset(pkey, 'score', score)
            if score > 0:
                heapq.heappush(self.pheap, (score, pkey.decode()))
        logger.info(
            f'{len(self.pheap)} proxies loaded. {total} scanned totally')

    def cal_score(self, stat):
        used_count = int(stat[b'used_count'])
        success_count = int(stat[b'success_count'])
        total_seconds = int(stat[b'total_seconds'])
        last_fail = stat[b'last_fail']
        timestamp = int(stat[b'timestamp'])
        score = float(stat[b'score'])
        if success_count == 0:
            return -used_count
        # features:
        # 1. success rate
        # 2. success count
        # 3. freshness
        # 4. last success
        # 5. speed
        # math.log(3600 * 24 * 180) = 16.56
        # math.log(3600 * 24 * 30) = 14.78
        # math.log(3600 * 24) = 11.37
        # math.log(3600) = 8.19
        return round(3 * float(success_count) / used_count +
                     1 * success_count + 0.25 *
                     (16.56 - math.log(time.time() - timestamp)) + 1 *
                     (1 if last_fail == b'' else 0) + 0.25 *
                     max(0, (15 - float(total_seconds) / success_count)))
