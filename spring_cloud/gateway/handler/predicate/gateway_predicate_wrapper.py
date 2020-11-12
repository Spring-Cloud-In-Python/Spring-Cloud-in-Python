# -*- coding: utf-8 -*-

__author__ = "Chaoyuuu (chaoyu2330@gmail.com)"
__license__ = "Apache 2.0"

# scip plugin
from spring_cloud.gateway.handler.predicate.gateway_predicate import GatewayPredicate
from spring_cloud.gateway.handler.predicate.predicate import Predicate


class GatewayPredicateWrapper(GatewayPredicate):
    def __init__(self, delegate: Predicate):
        self.__delegate = delegate
