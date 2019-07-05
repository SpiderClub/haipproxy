import argparse
import logging

from haipproxy.client.redis_ops import ProxyMaintainer

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    parser = argparse.ArgumentParser(description="redis ops")
    parser.add_argument("-d",
                        "--delete",
                        help="delete all failed proxies",
                        action="store_true")
    args = parser.parse_args()
    if args.delete:
        pm = ProxyMaintainer()
        pm.del_all_fails()
