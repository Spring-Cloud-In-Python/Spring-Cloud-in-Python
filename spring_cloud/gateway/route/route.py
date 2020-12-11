# -*- coding: utf-8 -*-
from __future__ import annotations

# standard library
from typing import List

__author__ = "Chaoyuuu (chaoyu2330@gmail.com)"
__license__ = "Apache 2.0"

# scip plugin
from spring_cloud.gateway.filter import GatewayFilter
from spring_cloud.gateway.handler.predicate import AND, NOT, OR, Predicate
from spring_cloud.utils.validate import not_none


class Route:
    def __init__(self, route_id: int, uri: str, order: int, predicate: Predicate, gateway_filters: [], metadata: {}):
        self.__route_id = route_id
        self.__uri = uri
        self.__order = order
        self.__predicate = predicate
        self.__gateway_filters = gateway_filters
        self.__metadata = metadata

    @property
    def route_id(self) -> int:
        return self.__route_id

    @property
    def uri(self) -> str:
        return self.__uri

    @property
    def order(self) -> int:
        return self.__order

    @property
    def predicate(self) -> Predicate:
        return self.__predicate

    @property
    def filters(self) -> []:
        return self.__gateway_filters

    @property
    def metadata(self) -> {}:
        return self.__metadata

    def builder(self):
        return Route.Builder()

    class Builder:
        def __init__(self):
            self.__route_id = None
            self.__uri = None
            self.__predicate = None
            self.__gateway_filters = []
            self.__metadata = {}
            self.__order = None

        def filters(self, gateway_filters: List) -> Route.Builder:
            self.__gateway_filters.extends(gateway_filters)
            return self

        def filter(self, gateway_filter: GatewayFilter) -> Route.Builder:
            self.__gateway_filters.append(gateway_filter)
            return self

        def set_route_id(self, route_id: str) -> Route.Builder:
            self.__route_id = route_id
            return self

        def set_uri(self, uri: str) -> Route.Builder:
            self.__uri = uri
            return self

        def set_predicate(self, predicate: Predicate) -> Route.Builder:
            self.__predicate = predicate
            return self

        def set_order(self, order: int) -> Route.Builder:
            self.__order = order
            return self

        def set_metadata(self, key: str, value: object) -> Route.Builder:
            self.__metadata[key] = value
            return self

        @property
        def predicate(self) -> Predicate:
            return self.__predicate

        def and_(self, predicate: Predicate) -> Route.Builder:
            self.__predicate = AND(self.__predicate, predicate)
            return self

        def or_(self, predicate: Predicate) -> Route.Builder:
            self.__predicate = OR(self.__predicate, predicate)
            return self

        def negate_(self) -> Route.Builder:
            self.__predicate = NOT(self.__predicate)
            return self

        def build(self) -> Route:
            not_none(self.__route_id)
            not_none(self.__uri)
            not_none(self.__predicate)
            return Route(
                self.__route_id, self.__uri, self.__order, self.__predicate, self.__gateway_filters, self.__metadata
            )
