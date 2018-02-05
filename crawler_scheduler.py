"""
This module is used to start spiders scheduler.
"""

from scheduler import TaskScheduler


if __name__ == '__main__':
    task_schduler = TaskScheduler('crawler')
    task_schduler.schedule_all_right_now()
    task_schduler.schedule_with_delay()