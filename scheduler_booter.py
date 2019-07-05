from haipproxy.scheduler import scheduler_start

if __name__ == '__main__':
    import logging
    logging.basicConfig(level=logging.INFO)
    scheduler_start()
