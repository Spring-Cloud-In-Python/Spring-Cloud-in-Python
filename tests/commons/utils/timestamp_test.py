# -*- coding: utf-8 -*-

__author__ = "Daniel1147 (sxn91401@gmail.com)"
__license__ = "Apache 2.0"

# standard library
import time

# scip plugin
from spring_cloud.commons.utils.timestamp import current_timestamp


def test_timestamp():
    start = current_timestamp()
    sleep_time = 0.1
    time.sleep(sleep_time)
    end = current_timestamp()

    assert end > start
    assert 0 < start

    acceptable_range = sleep_time * 1.5 * 1000  # in millisecond
    assert acceptable_range >= (end - start)
