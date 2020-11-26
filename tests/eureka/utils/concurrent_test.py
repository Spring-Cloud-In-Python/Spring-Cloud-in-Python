# -*- coding: utf-8 -*-

__author__ = "Haribo (haribo1558599@gmail.com)"
__license__ = "Apache 2.0"

# scip plugin
from eureka.utils.concurrent import ConcurrentCircularList


def test_append_to_concurrent_circular_list():
    concurrent_circular_list = ConcurrentCircularList()
    concurrent_circular_list.append(1)
    concurrent_circular_list.append(2)
    concurrent_circular_list.append(3)

    assert concurrent_circular_list._circular_list == [1, 2, 3]


def test_iterate_concurrent_circular_list():
    concurrent_circular_list = ConcurrentCircularList([1, 2, 3])

    assert next(concurrent_circular_list) == 1
    assert next(concurrent_circular_list) == 2
    assert next(concurrent_circular_list) == 3
    assert next(concurrent_circular_list) == 1
    assert next(concurrent_circular_list) == 2
    assert next(concurrent_circular_list) == 3


def test_iterate_empty_concurrent_circular_list():
    concurrent_circular_list = ConcurrentCircularList()
    try:
        next(concurrent_circular_list)
    except StopIteration:
        assert True
    else:
        assert False
