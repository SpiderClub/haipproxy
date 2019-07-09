import argparse
import logging

import schedule

from haipproxy.client import ProxyClient, SquidClient

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    parser = argparse.ArgumentParser(description="run proxy client")
    parser.add_argument("-d",
            "--delete",
            help="delete all failed proxies",
            action="store_true")
    parser.add_argument("-p",
            "--proxies",
            help="get valid proxy list",
            action="store_true")
    parser.add_argument("-s",
            "--squid",
            nargs='?',
            type=int,
            metavar='interval',
            help= """ Update squid conf periodically.  If you belong to admin group, you can start the task using the following cmd: python squid_update.py The default usage value is 'https' and interval value is 1 hour, use the following cmd if you want a different usage and updating interval sudo python3 run_client.py -s 60""")
    args = parser.parse_args()
    pc = ProxyClient()
    if args.delete:
        pc.del_all_fails()
    if args.proxies:
        for proxy in pc.next_proxy('https'):
            print(proxy)
        print('#################')
        for proxy in pc.next_proxy():
            print(proxy)
    if args.squid:
        logging.info('squid update is starting...')
        sc = SquidClient()
        sc.update_conf()
        schedule.every(args.squid).minutes.do(sc.update_conf)
        while True:
            schedule.run_pending()
            time.sleep(1)
