# -*- coding: utf-8 -*-

__author__ = "Chaoyuuu (chaoyu2330@gmail.com)"
__license__ = "Apache 2.0"

# scip plugin
from spring_cloud.gateway.handler.predicate.predicate import Predicate, StaticPredicate


class OrGatewayPredicate(Predicate):
    def __init__(self, p1: Predicate, p2: Predicate):
        self.p1 = p1
        self.p2 = p2

    def test(self, obj) -> bool:
        return self.p1.test(obj) or self.p2.test(obj)
