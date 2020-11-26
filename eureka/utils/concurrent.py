# -*- coding: utf-8 -*-

# standard library
import random

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
        self._circular_list = list_ or []

    def __iter__(self):
        return self

    @synchronized
    def __next__(self):
        if self._circular_list:
            self._current_index += 1
            self._current_index %= len(self._circular_list)
            return self._circular_list[self._current_index]
        raise StopIteration("The list is empty.")

    def append(self, item):
        self._circular_list.append(item)

    def filter(self, f):
        """
        Args:
            f: a predicate function that returns a boolean

        """
        self._circular_list = [item for item in self._circular_list if f(item)]

    def shuffle(self):
        random.shuffle(self._circular_list)
