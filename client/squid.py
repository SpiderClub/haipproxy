"""
Squid Client for spiders.
"""
import subprocess

# from logger import client_logger
from utils import get_redis_conn
from config.settings import (
    SQUID_BIN_PATH, SQUID_CONF_PATH,
    SQUID_TEMPLATE_PATH)
from .core import IPFetcherMixin


__all__ = ['SquidClient']


class SquidClient(IPFetcherMixin):
    default_conf_detail = "cache_peer {} parent {} 0 no-query weighted-round-robin weight=1 " \
                          "connect-fail-limit=2 allow-miss max-conn=5 name=proxy-{}"
    other_confs = ['request_header_access Via deny all', 'request_header_access X-Forwarded-For deny all',
                   'request_header_access From deny all', 'never_direct allow all']

    def __init__(self, task):
        super().__init__(task)
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
        with open(self.template_path, 'r') as fr, open(self.conf_path, 'w') as fw:
            original_conf = fr.read()
            if not proxies:
                fw.write(original_conf)
                # client_logger.info('no proxies got at this turn')
            else:
                conts.append(original_conf)
                # if two proxies use the same ip and different ports and no name
                # if assigned,cache_peer error will raise.
                for index, proxy in enumerate(proxies):
                    _, ip_port = proxy.split('://')
                    ip, port = ip_port.split(':')
                    conts.append(self.default_conf_detail.format(ip, port, index))
                conts.extend(self.other_confs)
                conf = '\n'.join(conts)
                fw.write(conf)
        # in docker, execute with shell will fail
        subprocess.call([self.squid_path, '-k', 'reconfigure'], shell=False)
        # client_logger.info('update squid conf successfully')