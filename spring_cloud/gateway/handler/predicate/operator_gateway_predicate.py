# -*- coding: utf-8 -*-

__author__ = "Chaoyuuu (chaoyu2330@gmail.com)"
__license__ = "Apache 2.0"

# scip plugin
from spring_cloud.gateway.handler.predicate.predicate import Predicate


class OrGatewayPredicate(Predicate):
    def __init__(self, p1: Predicate, p2: Predicate):
        self.p1 = p1
        self.p2 = p2

    def test(self, obj) -> bool:
        return self.p1.test(obj) or self.p2.test(obj)


class AndGatewayPredicate(Predicate):
    def __init__(self, p1: Predicate, p2: Predicate):
        self.p1 = p1
        self.p2 = p2

    def test(self, obj) -> bool:
        return self.p1.test(obj) and self.p2.test(obj)


class NegateGatewayPredicate(Predicate):
    def __init__(self, p: Predicate):
        self.p = p

    def test(self, obj) -> bool:
        return not self.p.test(obj)


def AND(p1: Predicate, p2: Predicate):
    return AndGatewayPredicate(p1, p2)


def OR(p1: Predicate, p2: Predicate):
    return OrGatewayPredicate(p1, p2)


def NOT(p: Predicate):
    return NegateGatewayPredicate(p)
