# -*- coding: utf-8 -*-
"""
Atomic types.

Feel free to add any feature in these utility types.
Currently, it only covers the feature we need.
"""
# standard library
import threading

__author__ = "Waterball (johnny850807@gmail.com)"
__license__ = "Apache 2.0"


class AtomicInteger:
    """
    An atomic integer
    """

    def __init__(self, value=0):
        self.__value = value
        self.__lock = threading.Lock()

    def increment_and_get(self) -> int:
        with self.__lock:
            self.__value += 1
            return self.__value

    def compare_and_set(self, expect: int, update: int) -> bool:
        with self.__lock:
            if self.__value == expect:
                self.__value = update
                return True
            else:
                return False

    def get(self):
        return self.__value
