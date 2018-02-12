import subprocess

from config.rules import RESOURCE_MAPS
from config.settings import VALIDATED_HTTPS_QUEUE
from utils.redis_util import get_redis_conn


class SquidClient:
    default_queue = 'https'
    default_conf_path = '/usr/local/etc/squid.conf'
    default_template_path = '/usr/local/etc/squid.conf.backup'
    default_batch_size = 500
    default_conf_detail = "cache_peer {} parent {} 0 no-query weighted-round-robin weight=2 " \
                          "connect-fail-limit=2 allow-miss max-conn=5 name=proxy-{}"

    def __init__(self, batch_size=None, queue=None, template_path=None, conf_path=None, squid_path=None):
        self.resource_queue = RESOURCE_MAPS.get('queue', VALIDATED_HTTPS_QUEUE) \
            if queue else VALIDATED_HTTPS_QUEUE
        self.template_path = template_path if template_path else self.default_template_path
        self.conf_path = conf_path if conf_path else self.default_conf_path
        self.batch_size = batch_size if batch_size else self.default_batch_size
        if not squid_path:
            try:
                r = subprocess.check_output('which squid', shell=True)
                self.squid_path = r.decode().strip()
            except subprocess.CalledProcessError:
                print('no squid is installed on this machine, or the installed dir '
                      'is not contained in environment path')
        else:
            self.squid_path = squid_path

    def update_conf(self):
        conn = get_redis_conn()
        proxies = conn.zrevrange(self.resource_queue, 0, self.batch_size)

        conts = list()
        with open(self.template_path, 'r') as fr, open(self.conf_path, 'w') as fw:
            conf = fr.read()

            # if two proxies use the same ip and different ports and no name if assigned,cache_peer error will raise.
            for index, value in enumerate(proxies):
                proxy = value.decode()
                _, ip_port = proxy.split('://')
                ip, port = ip_port.split(':')
                conts.append(self.default_conf_detail.format(ip, port, index))

            conf += '\n'.join(conts)
            conf += 'request_header_access Via deny all\n'
            conf += 'request_header_access X-Forwarded-For deny all\n'
            conf += 'request_header_access From deny all\n'
            conf += 'never_direct allow all\n'
            fw.write(conf)

        subprocess.call([self.squid_path, '-k', 'reconfigure'], shell=True)