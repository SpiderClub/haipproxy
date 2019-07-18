import asyncio
import heapq
import logging
import math
import subprocess
import threading
import time

from proxybroker import Broker

from haipproxy.utils import get_redis_conn, RedisOps
from haipproxy.config.settings import (
    SQUID_BIN_PATH,
    SQUID_CONF_PATH,
    SQUID_TEMPLATE_PATH,
    LOWEST_SCORE,
    MIN_PROXY_LEN,
)

logger = logging.getLogger(__name__)


class ProxyClient(object):
    def __init__(self):
        self.redis_conn = get_redis_conn()
        self.rpipe = self.redis_conn.pipeline()
        self.ppool = []
        self.idx = -1
        self.ro = RedisOps()
        # t = threading.Thread(target=self._refresh_periodically)
        # t.setDaemon(True)
        # t.start()

    def del_all_fails(self):
        total = 0
        nfail = 0
        for pkey in self.redis_conn.scan_iter(match='http*://*'):
            total += 1
            # if self.redis_conn.hget(pkey, 'fail') == b'badcontent':
            #     print(pkey)
            # else:
            #     continue
            score = float(self.redis_conn.hget(pkey, 'score'))
            if score <= LOWEST_SCORE - 2:
                self.rpipe.delete(pkey)
                nfail += 1
        self.rpipe.execute()
        logger.info(
            f'{nfail} failed proxies deleted, {total} before, {total - nfail} now '
        )

    def next_proxy(self, protocol=''):
        if not self.ppool:
            self._fill_pool()
        self.protocol = protocol.lower()
        if self.protocol != '':
            self.protocol += ':'
        while 1:
            self.idx = self.idx + 1
            if self.idx >= len(self.ppool):
                self.idx = -1
                raise StopIteration
            if self.ppool[self.idx][1].startswith(self.protocol):
                yield self.ppool[self.idx][1]

    def _refresh_periodically(self):
        while True:
            # lock
            self.ppool.clear()
            self._fill_pool()
            time.sleep(3600)

    def _fill_pool(self):
        total = 0
        for pkey in self.redis_conn.scan_iter(match='http*://*'):
            total += 1
            stat = self.redis_conn.hgetall(pkey)
            score = self.cal_score(stat)
            self.redis_conn.hset(pkey, 'score', score)
            if score > LOWEST_SCORE:
                heapq.heappush(self.ppool, (score, pkey.decode()))
        logger.info(
            f'{len(self.ppool)} proxies loaded. {total} scanned totally')

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
            2 * float(success_count) / used_count + 0.5 * success_count +
            0.25 * (16.56 - math.log(time.time() - timestamp)) + 1 *
            (2 if last_fail == b'' else -1) +
            0.20 * max(0, (15 - float(total_seconds) / success_count)), 2)

    def load_file(self, fname):
        with open(fname, 'r') as f:
            total = 0
            for line in f.readlines():
                total += 1
                proxy = line.strip()
                if len(proxy) < MIN_PROXY_LEN:
                    continue
                self.ro.set_proxy(proxy)
            logger.info(f'{total} lines')

    def dump_proxies(self, fname):
        with open(fname, 'w') as f:
            for p in self.next_proxy():
                f.write(p + '\n')

    async def _consume(self, aqu):
        """Save proxies to redis"""
        while True:
            proxy = await aqu.get()
            if proxy is None:
                logging.info('got None from proxies queue')
                break
            for protocol in proxy.types or ['http', 'https']:
                row = '%s://%s:%d' % (protocol, proxy.host, proxy.port)
                self.ro.set_proxy(row)
        self.ro.flush()

    def grab_proxybroker(self):
        aqu = asyncio.Queue()
        producer = Broker(aqu)
        tasks = asyncio.gather(
            producer.grab(),
            self._consume(aqu),
        )
        loop = asyncio.get_event_loop()
        loop.run_until_complete(tasks)


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
