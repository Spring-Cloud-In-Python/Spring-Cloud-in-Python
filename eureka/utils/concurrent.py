# -*- coding: utf-8 -*-

# pypi/conda library
from wrapt import synchronized

__author__ = "Haribo (haribo1558599@gmail.com)"
__license__ = "Apache 2.0"


class ConcurrentCircularList:
    """
    A simple thread-safe circular list which allows user
    iterate in a round-robin way.
    """

    def __init__(self, list_: list = None):
        self._current_index = -1
        self._circular_list = list_ if list_ else []

    def __iter__(self):
        return iter(self._circular_list)

    @synchronized
    def next(self):
        if len(self._circular_list) <= 0:
            return None

        self._current_index += 1
        self._current_index %= len(self._circular_list)

        return self._circular_list[self._current_index]

    def append(self, item):
        self._circular_list.append(item)
