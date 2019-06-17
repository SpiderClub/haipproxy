"""
Squid Client for spiders.
"""
import subprocess

# from logger import client_logger
from ..utils import get_redis_conn
from ..config.settings import (SQUID_BIN_PATH, SQUID_CONF_PATH,
                               SQUID_TEMPLATE_PATH, TTL_VALIDATED_RESOURCE,
                               LONGEST_RESPONSE_TIME, LOWEST_SCORE,
                               LOWEST_TOTAL_PROXIES)
from ..config.rules import (SCORE_MAPS, TTL_MAPS, SPEED_MAPS)
from .core import IPFetcherMixin

__all__ = ['SquidClient']


class SquidClient(IPFetcherMixin):
    default_conf_detail = "cache_peer {} parent {} 0 no-query weighted-round-robin weight=1 " \
                          "connect-fail-limit=2 allow-miss max-conn=5 name=proxy-{}"
    other_confs = [
        'request_header_access Via deny all',
        'request_header_access X-Forwarded-For deny all',
        'request_header_access From deny all', 'never_direct allow all'
    ]

    def __init__(self,
                 task,
                 score_map=SCORE_MAPS,
                 ttl_map=TTL_MAPS,
                 speed_map=SPEED_MAPS,
                 longest_response_time=LONGEST_RESPONSE_TIME,
                 lowest_score=LOWEST_SCORE,
                 ttl_validated_resource=TTL_VALIDATED_RESOURCE,
                 min_pool_size=LOWEST_TOTAL_PROXIES):
        if task not in score_map.keys():
            # client_logger.warning('task value is invalid, https task will be used')
            task = 'https'
        score_queue = score_map.get(task)
        ttl_queue = ttl_map.get(task)
        speed_queue = speed_map.get(task)
        super().__init__(score_queue, ttl_queue, speed_queue,
                         longest_response_time, lowest_score,
                         ttl_validated_resource, min_pool_size)
        self.template_path = SQUID_TEMPLATE_PATH
        self.conf_path = SQUID_CONF_PATH
        if not SQUID_BIN_PATH:
            try:
                r = subprocess.check_output('which squid', shell=True)
                self.squid_path = r.decode().strip()
            except subprocess.CalledProcessError:
                # client_logger.warning('no squid is installed on this machine, or the installed dir is not '
                #                       'contained in environment path')
                pass
        else:
            self.squid_path = SQUID_BIN_PATH

    def update_conf(self):
        conn = get_redis_conn()
        proxies = self.get_available_proxies(conn)
        conts = list()
        with open(self.template_path, 'r') as fr, open(self.conf_path,
                                                       'w') as fw:
            original_conf = fr.read()
            if not proxies:
                fw.write(original_conf)
                # client_logger.info('no proxies got at this turn')
            else:
                conts.append(original_conf)
                # if two proxies use the same ip and different ports and no name
                # is assigned, cache_peer error will raise.
                for index, proxy in enumerate(proxies):
                    _, ip_port = proxy.split('://')
                    ip, port = ip_port.split(':')
                    conts.append(
                        self.default_conf_detail.format(ip, port, index))
                conts.extend(self.other_confs)
                conf = '\n'.join(conts)
                fw.write(conf)
        # in docker, execute with shell will fail
        subprocess.call([self.squid_path, '-k', 'reconfigure'], shell=False)
        # client_logger.info('Squid conf is successfully updated')
