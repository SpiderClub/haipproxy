"""
Squid Client for spiders.
"""

import time
import subprocess

from config.rules import (
    SCORE_MAPS, TTL_MAPS,
    SPEED_MAPS)
from utils import (
    get_redis_conn, decode_all)
from config.settings import (
    SQUID_BIN_PATH, SQUID_CONF_PATH,
    SQUID_TEMPLATE_PATH, VALIDATED_HTTPS_QUEUE,
    TTL_HTTPS_QUEUE, TTL_VALIDATED_RESOURCE,
    SPEED_HTTPS_QUEUE, LONGEST_RESPONSE_TIME,
    LOWEST_SCORE)


class SquidClient:
    default_conf_detail = "cache_peer {} parent {} 0 no-query weighted-round-robin weight=1 " \
                          "connect-fail-limit=2 allow-miss max-conn=5 name=proxy-{}"
    other_confs = ['request_header_access Via deny all', 'request_header_access X-Forwarded-For deny all',
                   'request_header_access From deny all', 'never_direct allow all']

    def __init__(self, resource_queue=None, verified_queue=None, speed_queue=None):
        self.resource_queue = SCORE_MAPS.get(resource_queue) if resource_queue else VALIDATED_HTTPS_QUEUE
        self.verified_queue = TTL_MAPS.get(verified_queue) if verified_queue else TTL_HTTPS_QUEUE
        self.speed_queue = SPEED_MAPS.get(speed_queue) if speed_queue else SPEED_HTTPS_QUEUE
        self.template_path = SQUID_TEMPLATE_PATH
        self.conf_path = SQUID_CONF_PATH
        # todo consider whether the batch size is neccessary
        if not SQUID_BIN_PATH:
            try:
                r = subprocess.check_output('which squid', shell=True)
                self.squid_path = r.decode().strip()
            except subprocess.CalledProcessError:
                print('no squid is installed on this machine, or the installed dir '
                      'is not contained in environment path')
        else:
            self.squid_path = SQUID_BIN_PATH

    def update_conf(self):
        conn = get_redis_conn()
        start_time = int(time.time()) - TTL_VALIDATED_RESOURCE * 60
        pipe = conn.pipeline(False)
        pipe.zrevrangebyscore(self.resource_queue, '+inf', LOWEST_SCORE)
        pipe.zrevrangebyscore(self.verified_queue, '+inf', start_time)
        pipe.zrangebyscore(self.speed_queue, 0, 1000*LONGEST_RESPONSE_TIME)
        scored_proxies, verified_proxies, speed_proxies = pipe.execute()
        proxies = scored_proxies and verified_proxies and speed_proxies
        if not proxies:
            proxies = scored_proxies if scored_proxies else verified_proxies

        proxies = decode_all(proxies)

        conts = list()
        with open(self.template_path, 'r') as fr, open(self.conf_path, 'w') as fw:
            conts.append(fr.read())

            # if two proxies use the same ip and different ports and no name
            # if assigned,cache_peer error will raise.
            for index, proxy in enumerate(proxies):
                _, ip_port = proxy.split('://')
                ip, port = ip_port.split(':')
                conts.append(self.default_conf_detail.format(ip, port, index))
            conts.extend(self.other_confs)
            conf = '\n'.join(conts)
            fw.write(conf)

        subprocess.call([self.squid_path, '-k', 'reconfigure'], shell=True)
        print('update squid conf successfully')
