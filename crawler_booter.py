from haipproxy.scheduler import crawler_start

if __name__ == '__main__':
    import logging
    logging.basicConfig(level=logging.INFO)
    crawler_start()
