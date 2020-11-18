# -*- coding: utf-8 -*-
# standard library
from abc import ABC, abstractmethod

__author__ = "Chaoyuuu (chaoyu2330@gmail.com)"
__license__ = "Apache 2.0"

# scip plugin
from spring_cloud.gateway.filter.factory.filter import GatewayFilter


class GatewayFilterFactory(ABC):
    @abstractmethod
    def apply(self, config) -> GatewayFilter:
        pass


class AbstractGatewayFilterFactory(GatewayFilterFactory, ABC):
    pass
