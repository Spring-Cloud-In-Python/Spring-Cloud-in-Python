# -*- coding: utf-8 -*-

__author__ = "MJ (tsngmj@gmail.com)"
__license__ = "Apache 2.0"

# scip plugin
from ribbon.loadbalancer.abstract_loadbalance_rule import AbstractLoadBalanceRule
from ribbon.loadbalancer.server import Server


class BaseLoadBalancer(AbstractLoadBalanceRule):
    def __init__(self):
        pass

    def choose(self, key: object) -> Server:
        pass
