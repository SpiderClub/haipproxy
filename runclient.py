import argparse
import logging

import schedule

from haipproxy.client import ProxyClient, SquidClient
from haipproxy.monitor import start_prometheus

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    parser = argparse.ArgumentParser(description="run proxy client")

    parser.add_argument("-d",
                        "--delete",
                        help="delete all failed proxies",
                        action="store_true")
    parser.add_argument("-f",
                        "--flask",
                        help="run flask client",
                        action="store_true")
    parser.add_argument("-m",
                        "--monitor",
                        help="run prometheus client",
                        action="store_true")
    parser.add_argument("-p",
                        "--proxies",
                        help="get valid proxy list",
                        action="store_true")
    parser.add_argument(
        "-s",
        "--squid",
        nargs='?',
        type=int,
        metavar='interval',
        help="Update squid conf periodically: sudo python3 runclient.py -s 60")

    subparsers = parser.add_subparsers(dest='command')
    loadpar = subparsers.add_parser(
        'load',
        help='Load proxies',
        description='Load proxies from storages',
    )
    loadpar.add_argument('file',
                         type=str,
                         help='Load from file with 1 proxy per line')

    args = parser.parse_args()
    if args.command == 'load':
        pc = ProxyClient()
        pc.load_file(args.file)
    if args.delete:
        pc = ProxyClient()
        pc.del_all_fails()
    if args.flask:
        from haipproxy.flaskapp import app
        app.run(port=5000, host="127.0.0.1")
    if args.monitor:
        start_prometheus()
    if args.proxies:
        pc = ProxyClient()
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
            time.sleep(5)
