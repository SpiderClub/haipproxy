import subprocess

from config.rules import RESOURCE_MAPS
from utils.redis_util import get_redis_conn
from config.settings import (
    VALIDATED_HTTPS_QUEUE, SQUID_BIN_PATH,
    SQUID_CONF_PATH, SQUID_TEMPLATE_PATH,
    PROXY_BATCH_SIZE, SQUID_PROXIES_RESOURCE)


class SquidClient:
    default_queue = 'https'
    default_batch_size = 500
    default_conf_detail = "cache_peer {} parent {} 0 no-query weighted-round-robin weight=1 " \
                          "connect-fail-limit=1 allow-miss max-conn=5 name=proxy-{}"
    other_confs = ['request_header_access Via deny all', 'request_header_access X-Forwarded-For deny all',
                   'request_header_access From deny all', 'never_direct allow all']

    def __init__(self, queue=None):
        self.resource_queue = RESOURCE_MAPS.get(queue) if queue else SQUID_PROXIES_RESOURCE
        self.batch_size = PROXY_BATCH_SIZE
        self.template_path = SQUID_TEMPLATE_PATH
        self.conf_path = SQUID_CONF_PATH
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
        proxies = conn.zrevrange(self.resource_queue, 0, self.batch_size)
        conts = list()
        with open(self.template_path, 'r') as fr, open(self.conf_path, 'w') as fw:
            conts.append(fr.read())

            # if two proxies use the same ip and different ports and no name
            # if assigned,cache_peer error will raise.
            for index, value in enumerate(proxies):
                proxy = value.decode()
                _, ip_port = proxy.split('://')
                ip, port = ip_port.split(':')
                conts.append(self.default_conf_detail.format(ip, port, index))
            conts.extend(self.other_confs)
            conf = '\n'.join(conts)
            fw.write(conf)

        subprocess.call([self.squid_path, '-k', 'reconfigure'], shell=True)
        print('update squid conf successfully')
