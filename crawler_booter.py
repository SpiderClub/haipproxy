import logging
from haipproxy.scheduler import crawler_start

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    crawler_start()
