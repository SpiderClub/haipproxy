import time
import requests

from haipproxy.client import ProxyFetcher
from haipproxy.utils import get_redis_conn

from .configs import (SCORE_MAPS, TTL_MAPS, SPEED_MAPS, LONGEST_RESPONSE_TIME,
                      LOWEST_SCORE, TTL_VALIDATED_RESOURCE,
                      LOWEST_TOTAL_PROXIES, DATA_ALL, TOTAL_SUCCESS_REQUESTS)


class Crawler:
    timeout = 10
    success_req = TOTAL_SUCCESS_REQUESTS
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 '
        '(KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
        'Host': 'www.zhihu.com'
    }

    client_configs = {
        'strategy': 'greedy',
        'fast_response': 5,
        'score_map': SCORE_MAPS,
        'ttl_map': TTL_MAPS,
        'speed_map': SPEED_MAPS,
        'longest_response_time': LONGEST_RESPONSE_TIME,
        'lowest_score': LOWEST_SCORE,
        'ttl_validated_resource': TTL_VALIDATED_RESOURCE,
        'min_pool_size': LOWEST_TOTAL_PROXIES,
        'all_data': DATA_ALL,
        'redis_args': redis_args
    }

    def __init__(self, retries=5):
        self.retries = retries
        self.fetcher = ProxyFetcher('zhihu', **self.client_configs)
        self.redis_conn = get_redis_conn()
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
                resp = requests.get(url,
                                    headers=self.headers,
                                    proxies=proxy,
                                    timeout=self.timeout,
                                    verify=False)
                end = time.time() * 1000
                if '安全验证' in resp.text:
                    if proxy:
                        self.fetcher.proxy_feedback('failure',
                                                    proxy.get(self.scheme))
                    print(
                        'Current ip is blocked! The proxy is {}'.format(proxy))
                    tries += 1
                    continue
                else:
                    print('Request succeeded! The proxy is {}'.format(proxy))
                    # if you use greedy strategy, you must feedback
                    self.fetcher.proxy_feedback('success',
                                                proxy.get(self.scheme),
                                                int(end - start))
                    # not considering transaction
                    self.redis_conn.incr(self.success_req, 1)
                    return resp.text
            except Exception as e:
                print(e)
                print('Request failed!The proxy is {}'.format(proxy))
                # it's important to feedback, otherwise you may use the bad proxy next time
                self.fetcher.proxy_feedback('failure', proxy.get(self.scheme))
            tries += 1
        return None
