# the code is partially copied from https://github.com/windcode/zhihu-crawler-people

import json
import time
from multiprocessing import Pool

from bs4 import BeautifulSoup as BS

from haipproxy.utils import get_redis_conn
from examples.zhihu.crawler import Crawler

per_page = 20
info_max_process_num = 50
list_max_process_num = 10
host = 'https://www.zhihu.com'
waiting_set = 'zhihu:seeds:to_crawl'
seeds_all = 'zhihu:seeds:all'
info_set = 'zhihu:info:user'

# Not considering concurrent security
common_crawler = Crawler()


def init_db():
    redis_client = get_redis_conn(db=1)
    return redis_client


def get_info(url_token):
    """get user info"""
    url = '%s/people/%s/answers' % (host, url_token)
    html = common_crawler.get(url)
    print("parsing page's HTML……")
    if not html:
        return

    s = BS(html, 'html.parser')

    try:
        data = s.find('div', attrs={'id': 'data'})['data-state']
        data = json.loads(data)
        data = data['entities']['users'][url_token]
    except Exception:
        return None
    # filter data according to userType
    if data['userType'] != 'people':
        return None

    return data


def get_per_followers(url_token, page, sum_page):
    """crawl use's followers"""
    print('crawling page %d/%d ……' % (page, sum_page))
    followers = list()
    url = '%s/people/%s/followers?page=%d' % (host, url_token, page)
    html = common_crawler.get(url)
    s = BS(html, 'html.parser')

    try:
        data = s.find('div', attrs={'id': 'data'})['data-state']
        data = json.loads(data)
        items = data['people']['followersByUser'][url_token]['ids']
    except (AttributeError, TypeError):
        return list()
    for item in items:
        if item is not None and item is not False and item is not True and item != '知乎用户':
            print(item)
            followers.append(item)

    return followers


def get_followers(url_token, follower_count):
    # get all the followers of the specified url_token
    # return [] if user has no followers
    if follower_count == 0:
        return []

    sum_page = int((follower_count - 1) / per_page) + 1

    pool = Pool(processes=list_max_process_num)

    results = []
    for page in range(1, sum_page + 1):
        results.append(
            pool.apply_async(get_per_followers, (url_token, page, sum_page)))
    pool.close()
    pool.join()

    follower_list = []
    for result in results:
        follower_list += result.get()
    return follower_list


def start():
    redis_client = init_db()
    while not redis_client.scard(waiting_set):
        # block if there is no seed in waiting_set
        print('no seeds in waiting set {}'.format(waiting_set))
        time.sleep(0.1)

    # fetch seeds from waiting_set
    url_token = redis_client.spop(waiting_set).decode()

    print("crawling %s's user info……" % url_token)
    user = get_info(url_token)
    redis_client.sadd(info_set, user)
    print("crawling  %s's followers list……" % url_token)
    try:
        follower_list = get_followers(url_token, user['followerCount'])
    except (TypeError, AttributeError):
        return

    for follower in follower_list:
        if not redis_client.sismember(seeds_all, follower):
            pipe = redis_client.pipeline(False)
            pipe.sadd(waiting_set, follower)
            pipe.sadd(seeds_all, follower)
            pipe.execute()
    print("user {}'s info has being crawled".format(url_token))


if __name__ == '__main__':
    init_seeds = ['resolvewang', 'excited-vczh']
    redis_conn = init_db()
    redis_conn.sadd(waiting_set, *init_seeds)
    redis_conn.sadd(seeds_all, *init_seeds)
    while True:
        start()
