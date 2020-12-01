# -*- coding: utf-8 -*-

__author__ = "MJ (tsngmj@gmail.com)"
__license__ = "Apache 2.0"

# standard library
from abc import ABC, abstractmethod


class ServerListFilterFactory(ABC):
    @abstractmethod
    def create(self):
        pass
