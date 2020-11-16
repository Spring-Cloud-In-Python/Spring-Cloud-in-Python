# -*- coding: utf-8 -*-

__author__ = "Chaoyuuu (chaoyu2330@gmail.com)"
__license__ = "Apache 2.0"

# scip plugin
from spring_cloud.gateway.handler.predicate.operator_gateway_predicate import (
    AND,
    NOT,
    OR,
    AndGatewayPredicate,
    OrGatewayPredicate,
)
from spring_cloud.gateway.handler.predicate.predicate import FALSE, TRUE, StaticPredicate


class TestOrGatewayPredicate:
    def test_Given_T_or_F_When_test_Should_be_T(self):
        predicate = OR(TRUE, FALSE)
        value = predicate.test("whatever")
        assert value

    def test_Given_F_or_F_When_test_Should_be_F(self):
        predicate = OR(FALSE, FALSE)
        value = predicate.test("whatever")
        assert not value

    def test_Given_T_or_T_When_test_Should_be_T(self):
        predicate = OR(TRUE, TRUE)
        value = predicate.test("whatever")
        assert value

    def test_Given_F_or_T_When_test_Should_be_T(self):
        predicate = OR(FALSE, TRUE)
        value = predicate.test("whatever")
        assert value


class TestAndGatewayPredicate:
    def test_Given_T_and_T_When_test_Should_be_T(self):
        predicate = AND(TRUE, TRUE)
        value = predicate.test("whatever")
        assert value

    def test_Given_T_and_F_When_test_Should_be_F(self):
        predicate = AND(TRUE, FALSE)
        value = predicate.test("whatever")
        assert not value

    def test_Given_F_and_T_When_test_Should_be_F(self):
        predicate = AND(FALSE, TRUE)
        value = predicate.test("whatever")
        assert not value

    def test_Given_F_and_F_When_test_Should_be_F(self):
        predicate = AND(FALSE, FALSE)
        value = predicate.test("whatever")
        assert not value


class TestNegateGatewayPredicate:
    def test_Given_T_When_test_Should_be_F(self):
        predicate = NOT(TRUE)
        value = predicate.test("whatever")
        assert not value

    def test_Given_F_When_test_Should_be_T(self):
        predicate = NOT(FALSE)
        value = predicate.test("whatever")
        assert value
