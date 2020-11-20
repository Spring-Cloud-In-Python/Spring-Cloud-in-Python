# -*- coding: utf-8 -*-

__author__ = "MJ (tsngmj@gmail.com)"
__license__ = "Apache 2.0"

# scip plugin
from ribbon.loadbalancer.loadbalance_rule import LoadBalanceRule
from ribbon.loadbalancer.loadbalancer import LoadBalancer


class AbstractLoadBalanceRule(LoadBalanceRule):

    __lb = LoadBalancer()

    def set_loadbalancer(self, lb: LoadBalancer):
        self.__lb = lb

    def get_loadbalancer(self):
        return self.__lb
