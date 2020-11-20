# -*- coding: utf-8 -*-

__author__ = "MJ (tsngmj@gmail.com)"
__license__ = "Apache 2.0"

from abc import ABC, abstractmethod

from ribbon.loadbalancer.loadbalancer import LoadBalancer
from ribbon.loadbalancer.server import Server



"""
Interface that defines a "Rule" for a LoadBalancer. A Rule can be thought of
as a Strategy for loadbalacing. Well known loadbalancing strategies include
Round Robin, Response Time based etc.
"""
class LoadBalanceRule(ABC):
    @abstractmethod
    def choose(self, key: object) -> Server:
        pass

    @abstractmethod
    def set_loadbalancer(self, lb: LoadBalancer):
        pass

    @abstractmethod
    def get_loadbalancer(self):
        pass