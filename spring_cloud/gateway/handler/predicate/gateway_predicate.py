# -*- coding: utf-8 -*-
from __future__ import annotations

# standard library
from abc import ABC, abstractmethod

__author__ = "Chaoyuuu (chaoyu2330@gmail.com)"
__license__ = "Apache 2.0"

# scip plugin
from spring_cloud.gateway.handler.predicate.gateway_predicate_wrapper import GatewayPredicateWrapper
from spring_cloud.gateway.handler.predicate.or_gateway_predicate import OrGatewayPredicate
from spring_cloud.gateway.handler.predicate.predicate import Predicate


class GatewayPredicate(ABC, Predicate):
    def test(self, obj) -> bool:
        print("hii")
        return True

    def wrap_if_needed(self, other: Predicate) -> GatewayPredicate:

        if isinstance(other, GatewayPredicate):
            right = GatewayPredicate(other)
        else:
            right = GatewayPredicateWrapper(other)

        return right

    def or_predicate(self, other: Predicate) -> Predicate:
        """
        Gets all ServiceInstances associated with a particular serviceId.
        :param other:
        :return: A List of ServiceInstance.
        """
        return OrGatewayPredicate(self, self.wrap_if_needed(other))
