"""
This module is used to start multi spiders or validators from ide or cmd.

All the startup args can be found in config/rules.py, including:
CRAWLER_TASK_MAPS, VALIDATOR_TASK_MAPS

You can start proxy spiders using the following cmd:
python crawler_booter.py --usage crawler

If you want to start only common spider and ajax proxy spider, run:
python crawler_booter.py --usage crawler common ajax

While if you want to start all the validators, run:
python crawler_booter.py --usage validator

If you just want to start init and https validator, run:
python crawler_booter.py --usage validator init https
"""
from scheduler import crawler_start


if __name__ == '__main__':
    crawler_start()
