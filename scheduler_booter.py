"""
This module is used to start spider scheduler and validator scheduler.

You can start crawler scheduler using the following cmd:
python scheduler_booter.py --usage crawler

While if you want to start validator scheduler, run:
python scheduler_booter.py --usage validator
"""

from scheduler import scheduler_start


if __name__ == '__main__':
    scheduler_start()