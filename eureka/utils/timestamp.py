# -*- coding: utf-8 -*-

__author__ = "Daniel1147 (sxn91401@gmail.com)"
__license__ = "Apache 2.0"

# standard library
import math
import time


def current_milli_time():
    return int(math.floor(time.time() * 1000))


def current_timestamp() -> int:
    """

    :return: The timestamp of milliseconds
    """
    return current_milli_time()
