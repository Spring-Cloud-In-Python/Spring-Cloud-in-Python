# -*- coding: utf-8 -*-

__author__ = "Haribo (haribo1558599@gmail.com)"
__license__ = "Apache 2.0"

# pypi/conda library
import pytest

# scip plugin
from eureka.utils.concurrent import ConcurrentCircularList, ConcurrentMap


class TestConcurrentCircularList:
    def test_append_to_concurrent_circular_list(self):
        concurrent_circular_list = ConcurrentCircularList()
        concurrent_circular_list.append(1)
        concurrent_circular_list.append(2)
        concurrent_circular_list.append(3)

        assert concurrent_circular_list._circular_list == [1, 2, 3]

    def test_iterate_concurrent_circular_list(self):
        concurrent_circular_list = ConcurrentCircularList([1, 2, 3])

        assert next(concurrent_circular_list) == 1
        assert next(concurrent_circular_list) == 2
        assert next(concurrent_circular_list) == 3
        assert next(concurrent_circular_list) == 1
        assert next(concurrent_circular_list) == 2
        assert next(concurrent_circular_list) == 3

    def test_iterate_empty_concurrent_circular_list(self):
        concurrent_circular_list = ConcurrentCircularList()
        try:
            next(concurrent_circular_list)
        except StopIteration:
            assert True
        else:
            assert False


class TestConcurrentMap:
    def test_put_and_get(self):
        concurrent_map = ConcurrentMap()

        assert concurrent_map.get("absent key") is None

        concurrent_map.put("first", 1)
        concurrent_map.put("second", 2)
        assert concurrent_map.get("first") == 1
        assert concurrent_map.get("second") == 2

        concurrent_map.put("first", 3)
        assert concurrent_map.get("first") == 3

    def test_pub_if_absent(self):
        concurrent_map = ConcurrentMap()

        concurrent_map.put_if_absent("key", 1)
        assert concurrent_map.get("key") == 1

        concurrent_map.put_if_absent("key", 2)
        assert concurrent_map.get("key") == 1

    def test_return_of_put(self):
        concurrent_map = ConcurrentMap()
        assert concurrent_map.put("a", 1) == 1
        assert concurrent_map.put_if_absent("b", 2) == 2
        assert concurrent_map.put_if_absent("a", 3) == 1

    def test_entry_set(self):
        concurrent_map = ConcurrentMap()
        concurrent_map.put("1", 1)
        concurrent_map.put("2", 2)
        concurrent_map.put("3", 3)

        assert  list(concurrent_map.entry_set()) == [("1", 1), ("2", 2), ("3", 3)]
