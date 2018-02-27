"""
This module provides exceptions may be raised in haipproxy
"""


class TaskNotRegister(Exception):
    """Raise when the task is not registered in task maps in ../config/rules.py"""
