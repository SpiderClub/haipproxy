import argparse
import logging

import schedule

from haipproxy.client import ProxyClient, SquidClient
from haipproxy.monitor import start_prometheus

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    parser = argparse.ArgumentParser(description="run proxy client")
    subparsers = parser.add_subparsers(dest='command')

    redispar = subparsers.add_parser(
        'redis',
        help='Redis operations',
    )
    redispar.add_argument('-d',
                          "--delete",
                          help="delete all failed proxies",
                          action="store_true")
    redispar.add_argument('-s',
                          '--stat',
                          help='Stat of redis',
                          action="store_true")

    filepar = subparsers.add_parser(
        'file',
        help='Load or dump proxy file',
    )
    filepar.add_argument('-l',
                         '--load',
                         help='Load from file with 1 proxy per line',
                         action='store_true')
    filepar.add_argument('-d',
                         '--dump',
                         help='Dump good proxies to a file',
                         action='store_true')
    filepar.add_argument('file', type=str, help='file path')

    invokepar = subparsers.add_parser(
        'invoke',
        help='invoke 3rd party libs',
    )
    invokepar.add_argument('lib', type=str, help='3rd party library name')

    prometheuspar = subparsers.add_parser('prometheus',
                                          help="run prometheus client")
    flaskpar = subparsers.add_parser('flask', help="run flask client")

    squidpar = subparsers.add_parser(
        'squid',
        help=
        'Update squid conf periodically: sudo python3 runclient.py squid 60')
    squidpar.add_argument('interval', type=int, help='update interval')

    args = parser.parse_args()
    if args.command == 'redis':
        pc = ProxyClient()
        if args.delete:
            pc.del_all_fails()
        elif args.stat:
            pass
    elif args.command == 'file':
        pc = ProxyClient()
        if args.load:
            pc.load_file(args.file)
        elif args.dump:
            pc.dump_proxies(args.file)
    elif args.command == 'invoke':
        pc = ProxyClient()
        if args.lib == 'proxybroker':
            pc.grab_proxybroker()
    elif args.command == 'prometheus':
        start_prometheus()
    elif args.command == 'flask':
        from haipproxy.flaskapp import app
        app.run(port=5000, host="127.0.0.1")
    elif args.command == 'squid':
        logging.info('squid update is starting...')
        sc = SquidClient()
        sc.update_conf()
        schedule.every(args.interval).minutes.do(sc.update_conf)
        while True:
            schedule.run_pending()
            time.sleep(5)
    else:
        print_help()
