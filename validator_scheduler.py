"""
This module is used to start validators scheduler.
"""

from scheduler import ValidatorScheduler


if __name__ == '__main__':
    task_schduler = ValidatorScheduler('validator')
    task_schduler.schedule_all_right_now()
    task_schduler.schedule_with_delay()