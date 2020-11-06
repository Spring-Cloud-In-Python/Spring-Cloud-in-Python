# -*- coding: utf-8 -*-

"""
A cache manager wrapper that supports some syntax sugar.

Usage:
    value = cache_manager.get(cache_key) \
                .on_cache_miss(lambda: retrieve_value(key))
"""


__author__ = "Waterball (johnny850807@gmail.com)"
__license__ = "Apache 2.0"

# standard library
from abc import ABC, abstractmethod


class OnCacheMiss:
    def __init__(self, cache_manager, key, value):
        self.__cache_manager = cache_manager
        self.__key = key
        self.__value = value

    @abstractmethod
    def on_cache_miss(self, cache_miss_func):
        """
        :param cache_miss_func: (lambda ()->value)
        """
        if not self.__value:
            value = cache_miss_func()
            self.__cache_manager.put(self.__key, value)
            return value
        return self.__value


class CacheManager(ABC):
    """
    Service Provider Interface (SPI) for basic caching.
    We might want to extend this class with many features in the future.
    """

    def get(self, key) -> OnCacheMiss:
        value = self.retrieve_value(key)
        return OnCacheMiss(self, key, value)

    @abstractmethod
    def retrieve_value(self, key):
        pass

    @abstractmethod
    def put(self, key, value):
        pass


class NaiveCacheManager(CacheManager):
    """
    A very simple cache implementation that is not concerned about evict-and-replacement.
    """

    def __init__(self):
        self.cache_dict = {}

    def retrieve_value(self, key):
        return self.cache_dict.get(key, None)

    def put(self, key, value):
        self.cache_dict[key] = value
