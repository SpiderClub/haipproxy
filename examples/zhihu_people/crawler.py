import requests

from client import ProxyFetcher


class Crawler:
    timeout = 10
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
        'Host': 'www.zhihu.com'
    }

    def __init__(self, proxy_mode=0, retries=3):
        self.proxy_mode = proxy_mode
        self.retries = retries
        self.fetcher = ProxyFetcher('zhihu', strategy='greedy')

    def get(self, url):
        proxy = {'https': self.fetcher.get_proxy()} if self.proxy_mode else None
        tries = 0
        while tries < self.retries:
            try:
                resp = requests.get(url, headers=self.headers, proxies=proxy, timeout=self.timeout)
                return resp.text
            except Exception as e:
                print(e)
                self.fetcher.proxy_feedback(url, 'failure')
            tries += 1

        return None
