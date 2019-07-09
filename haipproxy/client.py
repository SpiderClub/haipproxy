import heapq
import logging
import math
import subprocess
import threading
import time

from haipproxy.utils import get_redis_conn
from haipproxy.config.settings import (SQUID_BIN_PATH, SQUID_CONF_PATH,
                                       SQUID_TEMPLATE_PATH,
                                       LONGEST_RESPONSE_TIME, LOWEST_SCORE,
                                       LOWEST_TOTAL_PROXIES)

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
        return round(
            2 * float(success_count) / used_count + 0.5 * success_count + 0.25 *
            (16.56 - math.log(time.time() - timestamp)) + 1 *
            (2 if last_fail == b'' else -1) +
            0.20 * max(0, (15 - float(total_seconds) / success_count)), 2)


class SquidClient(object):
    default_conf_detail = "cache_peer {} parent {} 0 no-query weighted-round-robin weight=1 " \
                          "connect-fail-limit=2 allow-miss max-conn=5 name=proxy-{}"
    other_confs = [
        'request_header_access Via deny all',
        'request_header_access X-Forwarded-For deny all',
        'request_header_access From deny all', 'never_direct allow all'
    ]

    def __init__(self):
        self.tmp_path = SQUID_TEMPLATE_PATH
        self.conf_path = SQUID_CONF_PATH
        r = subprocess.check_output('which squid', shell=True)
        self.squid_path = r.decode().strip()

    def update_conf(self):
        with open(self.tmp_path, 'r') as fr, open(self.conf_path, 'w') as fw:
            fw.write(fr.read())
            pc = ProxyClient()
            idx = 0
            for proxy in pc.next_proxy():
                _, ip_port = proxy.split('://')
                ip, port = ip_port.split(':')
                fw.write('\n')
                fw.write(self.default_conf_detail.format(ip, port, idx))
            fw.write('\n')
            fw.write('\n'.join(self.other_confs))
        # in docker, execute with shell will fail
        subprocess.call([self.squid_path, '-k', 'reconfigure'], shell=False)
        logger.info('Squid conf is successfully updated')
