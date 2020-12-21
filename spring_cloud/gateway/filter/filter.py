# -*- coding: utf-8 -*-
# standard library
from abc import ABC, abstractmethod

__author__ = "Chaoyuuu (chaoyu2330@gmail.com)"
__license__ = "Apache 2.0"

# scip plugin
from spring_cloud.gateway.server import ServerWebExchange


class GatewayFilterChain(ABC):
    @abstractmethod
    def filter(self, exchange: ServerWebExchange) -> None:
        pass


class GatewayFilter(ABC):
    @abstractmethod
    def filter(self, exchange: ServerWebExchange, chain: GatewayFilterChain) -> None:
        pass


class GlobalFilter(ABC):
    @abstractmethod
    def filter(self, exchange: ServerWebExchange, chain: GatewayFilterChain) -> None:
        pass


class StaticGatewayFilterChain(GatewayFilterChain):
    def filter(self, exchange: ServerWebExchange) -> None:
        pass
