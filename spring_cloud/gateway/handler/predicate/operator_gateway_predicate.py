# -*- coding: utf-8 -*-

__author__ = "Chaoyuuu (chaoyu2330@gmail.com)"
__license__ = "Apache 2.0"

from .predicate import Predicate


class OrGatewayPredicate(Predicate):
    def __init__(self, left: Predicate, right: Predicate):
        self.left = left
        self.right = right

    def test(self, obj) -> bool:
        return self.left.test(obj) or self.right.test(obj)

    def __str__(self):
        return f"({self.left} || {self.right})"


class AndGatewayPredicate(Predicate):
    def __init__(self, left: Predicate, right: Predicate):
        self.left = left
        self.right = right

    def test(self, obj) -> bool:
        return self.left.test(obj) and self.right.test(obj)

    def __str__(self):
        return f"({self.left} && {self.right})"


class NegateGatewayPredicate(Predicate):
    def __init__(self, p: Predicate):
        self.p = p

    def test(self, obj) -> bool:
        return not self.p.test(obj)

    def __str__(self):
        return f"!{self.p}"


def AND(left: Predicate, right: Predicate) -> Predicate:
    return AndGatewayPredicate(left, right)


def OR(left: Predicate, right: Predicate) -> Predicate:
    return OrGatewayPredicate(left, right)


def NOT(p: Predicate) -> Predicate:
    return NegateGatewayPredicate(p)
