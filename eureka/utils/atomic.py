# -*- coding: utf-8 -*-

# pypi/conda library
from wrapt import synchronized

__author__ = "Haribo (haribo1558599@gmail.com)"
__license__ = "Apache 2.0"


class AtomicInteger:
    def __init__(self, value: int = 0):
        self._value = value

    def __str__(self):
        return str(self._value)

    def get(self) -> int:
        return self._value

    def set(self, value: int):
        self._value = value

    @synchronized
    def increment_and_get(self):
        self._value += 1
        return self._value
