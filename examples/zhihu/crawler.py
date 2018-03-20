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

    def __init__(self, retries=5):
        self.retries = retries
        self.fetcher = ProxyFetcher('zhihu', strategy='greedy')
        self.conn = get_redis_conn(db=1)
        self.scheme = 'https'

    def get(self, url):
        tries = 0
        while tries < self.retries:
            proxy = {self.scheme: self.fetcher.get_proxy()}
            while not proxy.get(self.scheme):
                time.sleep(0.5)
                proxy = {self.scheme: self.fetcher.get_proxy()}

            try:
                start = time.time() * 1000
                resp = requests.get(url, headers=self.headers, proxies=proxy,
                                    timeout=self.timeout, verify=False)
                end = time.time() * 1000
                if '安全验证' in resp.text:
                    if proxy:
                        self.fetcher.proxy_feedback('failure', proxy.get(self.scheme))
                    print('Current ip is blocked! The proxy is {}'.format(proxy))
                    tries += 1
                    continue
                else:
                    print('Request succeeded! The proxy is {}'.format(proxy))
                    # if you use greedy strategy, you must feedback
                    self.fetcher.proxy_feedback('success', proxy.get(self.scheme), int(end - start))
                    # not considering transaction
                    self.conn.incr(self.success_req, 1)
                    self.conn.rpush(self.cur_time, int(end / 1000))
                    return resp.text
            except Exception as e:
                print(e)
                print('Request failed!The proxy is {}'.format(proxy))
                # it's important to feedback, otherwise you may use the bad proxy next time
                self.fetcher.proxy_feedback('failure', proxy.get(self.scheme))
            tries += 1
        return None
