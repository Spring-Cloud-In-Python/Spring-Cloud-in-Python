# -*- coding: utf-8 -*-
# standard library
from abc import ABC, abstractmethod

__author__ = "Chaoyuuu (chaoyu2330@gmail.com)"
__license__ = "Apache 2.0"


class Predicate(ABC):
    @abstractmethod
    def test(self, obj) -> bool:
        pass


class StaticPredicate(Predicate):
    def __init__(self, value: bool):
        self.value = value

    def test(self, obj) -> bool:
        return self.value
