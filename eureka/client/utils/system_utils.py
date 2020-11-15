# -*- coding: utf-8 -*-

# standard library
import time

__author__ = "Haribo (haribo1558599@gmail.com)"
__license__ = "Apache 2.0"


def current_time_in_millis() -> int:
    return int(round(time.time() * 1000))
