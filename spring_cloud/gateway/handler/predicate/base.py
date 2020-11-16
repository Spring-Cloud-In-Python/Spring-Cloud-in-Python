# -*- coding: utf-8 -*-
# standard library
from abc import ABC, abstractmethod

__author__ = "Chaoyuuu (chaoyu2330@gmail.com)"
__license__ = "Apache 2.0"

# scip plugin
from spring_cloud.gateway.handler.predicate.predicate import Predicate


class RoutePredicateFactory(ABC):
    @abstractmethod
    def apply(self, config) -> Predicate:
        pass


class AbstractRoutePredicateFactory(RoutePredicateFactory, ABC):
    pass
