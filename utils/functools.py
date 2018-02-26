"""
This module provides useful functions.
"""


def decode_all(res):
    """decode all results fetched from redis"""
    return list(map(bytes.decode, res))