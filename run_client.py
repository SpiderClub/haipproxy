import argparse
import logging

from haipproxy.client import ProxyClient

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    parser = argparse.ArgumentParser(description="redis ops")
    parser.add_argument("-d",
            "--delete",
            help="delete all failed proxies",
            action="store_true")
    parser.add_argument("-p",
            "--proxies",
            help="get valid proxy list",
            action="store_true")
    args = parser.parse_args()
    pc = ProxyClient()
    if args.delete:
        pc.del_all_fails()
    if args.proxies:
        for i in pc.next_proxy('https'):
            print(i)
        print('#################')
        for i in pc.next_proxy():
            print(i)
