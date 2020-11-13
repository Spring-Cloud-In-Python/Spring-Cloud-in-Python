# -*- coding: utf-8 -*-

__author__ = "Daniel1147 (sxn91401@gmail.com)"
__license__ = "Apache 2.0"

# standard library
import time

# scip plugin
from spring_cloud.commons.utils.timestamp import current_timestamp


def test_timestamp():
    start = current_timestamp()
    time.sleep(1)
    end = current_timestamp()

    assert end > start
    assert 0 < start

    acceptable_range = 1000 * 1.05
    assert acceptable_range >= (end - start)
