import json
import time
from multiprocessing import Pool

import redis
from bs4 import BeautifulSoup as BS

from examples.zhihu_people.crawler import Crawler

per_page = 20
info_max_process_num = 50  # 50
list_max_process_num = 10  # 10
host = 'https://www.zhihu.com'
waiting_set = 'info:seeds:to_crawl'
seeds_all = 'info:seeds:all'
info_set = 'info:user'


def init_db():
    redis_client = redis.Redis(host='127.0.0.1', port=6379, password='123456', db=0)
    return redis_client


def get_info(crawler, url_token):
    """获取某用户的个人信息"""
    url = '%s/people/%s/answers' % (host, url_token)
    html = crawler.get(url)
    print('正在解析用户页面HTML……')
    s = BS(html, 'html.parser')

    # 获得该用户藏在主页面中的json格式数据集
    try:
        data = s.find('div', attrs={'id': 'data'})['data-state']
        data = json.loads(data)
        data = data['entities']['users'][url_token]
    except Exception:
        return None
    # 只抓取people类型用户
    if data['userType'] != 'people':
        return None

    return data


def get_per_followers(url_token, page, sum_page):
    """抓取 follower 列表的每一页"""
    print('正在抓取第 %d/%d 页……' % (page, sum_page))
    followers = list()
    crawler = Crawler()
    url = '%s/people/%s/followers?page=%d' % (host, url_token, page)
    html = crawler.get(url)
    s = BS(html, 'html.parser')

    # 获得当前页的所有关注用户
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
    # 获取该用户的所有关注用户
    # 该用户没有关注人，直接返回空列表，退出
    if follower_count == 0:
        return []

    # 计算总页数
    sum_page = int((follower_count - 1) / per_page) + 1

    # 创建进程池
    pool = Pool(processes=list_max_process_num)

    # 抓取每一页的用户链接
    start_time = time.clock()
    results = []
    for page in range(1, sum_page + 1):
        # print('将第 %d/%d 页抓取进程加入进程池……' % (page, sum_page))
        results.append(pool.apply_async(get_per_followers, (url_token, page, sum_page)))
    # 关闭进程池，使其不再接受请求
    pool.close()
    # 等待所有进程请求执行完毕
    pool.join()
    end_time = time.clock()
    print('所有进程抓取完毕')
    total_time = float(end_time - start_time)
    print('总用时 : %f s' % total_time)
    print('平均每个进程用时 : %f s' % (total_time / sum_page))

    # 获取抓取结果
    print('获取抓取结果……')
    follower_list = []
    for result in results:
        follower_list += result.get()

    print('抓取到的用户 %s 的关注列表总人数为 %d 人！' % (url_token, len(follower_list)))
    print(follower_list)
    return follower_list


def start():
    redis_client = init_db()
    # 待抓取节点集合是否为空
    while not redis_client.scard(waiting_set):
        print('待抓取集合为空...')
        time.sleep(5)

    # 从待抓取节点集合随机取出一个节点
    url_token = redis_client.spop(waiting_set).decode()
    # 抓取节点代表用户的个人主页
    print('正在抓取用户 %s 的个人信息……' % url_token)
    crawler = Crawler()
    user = get_info(crawler, url_token)
    redis_client.sadd(info_set, user)
    # 开始抓取该用户 follower 列表
    print('开始抓取该用户的粉丝列表……')
    try:
        follower_list = get_followers(url_token, user['followerCount'])
    except (TypeError, AttributeError):
        return

    # 将 follower 列表中用户加入到待抓取集合
    push_success_num = 0
    for follower in follower_list:
        # 如果该用户都不存在于三大集合，则插入到待抓取集合中
        if not redis_client.sismember(seeds_all, follower):
            redis_client.sadd(waiting_set, follower)
            redis_client.sadd(seeds_all, follower)
            push_success_num += 1

    print('向待抓取节点集合中添加了 %d 人！' % push_success_num)
    print('目前待抓取节点集合中有 %d 人' % redis_client.scard(waiting_set))

    print('将用户 %s 放入列表抓取成功节点集合' % url_token)
    print('用户 %s 关注列表抓取完毕' % url_token)


if __name__ == '__main__':
    init_seeds = ['liu-meng-yuan-72-95']
    redis_conn = init_db()
    redis_conn.sadd(waiting_set, *init_seeds)
    redis_conn.sadd(seeds_all, *init_seeds)
    while True:
        start()
