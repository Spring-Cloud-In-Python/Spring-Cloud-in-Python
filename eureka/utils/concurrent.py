# -*- coding: utf-8 -*-

# standard library
import random
import threading
from typing import Callable, NoReturn

# pypi/conda library
from wrapt import synchronized

__author__ = "Haribo (haribo1558599@gmail.com)"
__license__ = "Apache 2.0"


class ConcurrentCircularList:
    """
    A simple thread-safe circular list which allows user
    iterate in a round-robin way by next().
    """

    def __init__(self, list_: list = None):
        self._current_index = -1
        self._circular_list = list_ or []

    def __iter__(self):
        """
        Returns: iterator of the original list instead of self to avoid infinite loop.

        """
        return iter(self._circular_list)

    @synchronized
    def __next__(self):
        if self._circular_list:
            self._current_index += 1
            self._current_index %= len(self._circular_list)
            return self._circular_list[self._current_index]
        raise StopIteration("The list is empty.")

    def __len__(self):
        return len(self._circular_list)

    def append(self, item):
        self._circular_list.append(item)

    def filter(self, f: Callable[[object], bool]) -> NoReturn:
        """
        Args:
            f: a predicate function that returns a boolean

        """
        if isinstance(f, Callable):
            self._circular_list = [item for item in self._circular_list if f(item)]
        else:
            raise TypeError(f"{f} is not Callable.")

    def shuffle(self):
        random.shuffle(self._circular_list)


class ConcurrentMap:
    def __init__(self):
        self.lock = threading.RLock()
        self.map = {}

    def get(self, key: str):
        with self.lock:
            if key not in self.map:
                return None

            return self.map[key]

    def put(self, key: str, value):
        with self.lock:
            self.map[key] = value

            return self.map[key]

    def put_if_absent(self, key: str, value):
        with self.lock:
            if key not in self.map:
                self.map[key] = value

            return self.map[key]

    def entry_set(self):
        with self.lock:
            return list(self.map.items())

    def size(self) -> int:
        with self.lock:
            return len(self.map)

    def remove(self, key: str):
        with self.lock:
            if key not in self.map:
                return None

            removed = self.map[key]
            del self.map[key]

            return removed
