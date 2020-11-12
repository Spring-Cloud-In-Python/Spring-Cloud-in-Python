# -*- coding: utf-8 -*-

__author__ = "Chaoyuuu (chaoyu2330@gmail.com)"
__license__ = "Apache 2.0"

# scip plugin
from spring_cloud.gateway.handler.predicate.gateway_predicate import GatewayPredicate
from spring_cloud.gateway.handler.predicate.or_gateway_predicate import OrGatewayPredicate
from spring_cloud.gateway.handler.predicate.predicate import StaticPredicate


def test_1():
    predicate = OrGatewayPredicate(StaticPredicate(True), StaticPredicate(False))
    value = predicate.test("whatever")
    assert value


def test_2():
    predicate = OrGatewayPredicate(StaticPredicate(False), StaticPredicate(False))
    value = predicate.test("whatever")
    assert not value


def test_3():
    predicate = OrGatewayPredicate(StaticPredicate(True), StaticPredicate(True))
    value = predicate.test("whatever")
    assert value


def test_4():
    predicate = GatewayPredicate()
    value = predicate.test("whatever")
    assert value
