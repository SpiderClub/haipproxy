"""
This module is used to start spider scheduler and validator scheduler.

You can start crawler scheduler using the following cmd:
python scheduler_booter.py --usage crawler

If you want to start common scheduler only, run:
python scheduler_booter.py --usage crawler common

While if you want to start validator scheduler, run:
python scheduler_booter.py --usage validator

Notice that the scheduler doesn't schedule init queue.
If you want to start https validator only, run:
python scheduler_booter.py --usage validator https
"""

from scheduler import scheduler_start


if __name__ == '__main__':
    scheduler_start()