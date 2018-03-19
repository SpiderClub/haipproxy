import time
import requests

from client import ProxyFetcher
from utils import get_redis_conn


class Crawler:
    timeout = 10
    success_req = 'zhihu:success:request'
    cur_time = 'zhihu:success:time'
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
        'Host': 'www.zhihu.com'
    }

    def __init__(self, proxy_mode=1, retries=5):
        self.proxy_mode = proxy_mode
        self.retries = retries
        self.fetcher = ProxyFetcher('zhihu', strategy='greedy')
        self.conn = get_redis_conn(db=1)

    def get(self, url):
        proxy = None
        tries = 0
        while tries < self.retries:
            if self.proxy_mode:
                proxy = {'https': self.fetcher.get_proxy()}
                while not proxy:
                    time.sleep(1)
                    proxy = {'https': self.fetcher.get_proxy()}

            try:
                start = time.time() * 1000
                resp = requests.get(url, headers=self.headers, proxies=proxy, timeout=self.timeout)
                end = time.time() * 1000
                if '安全验证' in resp.text:
                    self.fetcher.proxy_feedback('failure', proxy)
                    tries += 1
                    continue
                else:
                    print('Request succeeded! The proxy is {}'.format(proxy))
                    # if you use greedy strategy, you must feedback
                    self.fetcher.proxy_feedback('success', proxy, int(end-start))
                    # not considering transaction
                    self.conn.incr(self.success_req, 1)
                    self.conn.rpush(self.cur_time, int(end/1000))
                    return resp.text
            except Exception as e:
                print(e)
                # it's important to feedback, otherwise you may use the bad proxy next time
                self.fetcher.proxy_feedback('failure', proxy)
            tries += 1
        return None
