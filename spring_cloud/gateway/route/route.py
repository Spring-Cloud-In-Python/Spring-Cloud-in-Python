# -*- coding: utf-8 -*-
from __future__ import annotations

__author__ = "Chaoyuuu (chaoyu2330@gmail.com)"
__license__ = "Apache 2.0"

# scip plugin
from spring_cloud.gateway.filter import GatewayFilter
from spring_cloud.gateway.handler.predicate import Predicate
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
    def filter(self) -> []:
        return self.__gateway_filters

    @property
    def metadata(self) -> {}:
        return self.__metadata

    class Builder:
        def __init__(self):
            self.__route_id = None
            self.__uri = None
            self.__predicate = None
            self.__gateway_filters = []
            self.__metadata = {}
            self.__order = None

        def filters(self, gateway_filters: []) -> Route.Builder:
            self.__gateway_filters.extends(gateway_filters)
            return self

        def filter(self, gateway_filter: GatewayFilter) -> Route.Builder:
            self.__gateway_filters.append(gateway_filter)
            return self

        def set_route_id(self, route_id: int) -> Route.Builder:
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

        def set_metadata(self, metadata: {}) -> Route.Builder:
            self.__metadata = metadata
            return self

        # TODO: and_predicate() is a function to call Predicate.and_predicate(),
        #  but it has not been implemented, and will be done in the future.
        #  Same situation to or_predicate() and negate_predicate()
        def and_predicate(self, predicate: Predicate) -> Route.Builder:
            return self

        def or_predicate(self, predicate: Predicate) -> Route.Builder:
            return self

        def negate_predicate(self) -> Route.Builder:
            return self

        def build(self) -> Route:
            not_none(self.__route_id)
            not_none(self.__uri)
            not_none(self.__predicate)
            return Route(
                self.__route_id, self.__uri, self.__order, self.__predicate, self.__gateway_filters, self.__metadata
            )
