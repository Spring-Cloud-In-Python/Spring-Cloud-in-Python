# -*- coding: utf-8 -*-
# standard library
from abc import ABC, abstractmethod

__author__ = "Chaoyuuu (chaoyu2330@gmail.com)"
__license__ = "Apache 2.0"


class GatewayFilter(ABC):
    @abstractmethod
    def filter(self, exchange, chain):
        # return Mono<void>
        pass
