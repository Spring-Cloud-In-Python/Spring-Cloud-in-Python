# -*- coding: utf-8 -*-
from __future__ import annotations

__author__ = "Chaoyuuu (chaoyu2330@gmail.com)"
__license__ = "Apache 2.0"

# scip plugin
from spring_cloud.gateway.handler.predicate.predicate import Predicate
from spring_cloud.utils.validate import not_none


class Route:
    def __init__(self, route_id, uri, order, predicate, gateway_filters, metadata):
        self.route_id = route_id
        self.uri = uri
        self.order = order
        self.predicate = predicate
        self.gateway_filters = gateway_filters
        self.metadata = metadata

    def get_route_id(self) -> int:
        return self.route_id

    def get_uri(self) -> str:
        return self.uri

    def get_order(self) -> int:
        return self.order

    def get_predicate(self) -> Predicate:
        return self.predicate

    def get_filter(self) -> []:
        return self.gateway_filters

    def get_metadata(self) -> {}:
        return self.metadata

    class Builder:
        def __init__(self):
            self.route_id = None
            self.uri = None
            self.predicate = None
            self.gateway_filters = []
            self.metadata = {}
            self.order = None

        def filters(self, gateway_filters) -> Route.Builder:
            self.gateway_filters.extends(gateway_filters)
            return self

        def filter(self, gateway_filter) -> Route.Builder:
            self.gateway_filters.append(gateway_filter)
            return self

        def set_route_id(self, route_id: int) -> Route.Builder:
            self.route_id = route_id
            return self

        def set_uri(self, uri: str) -> Route.Builder:
            self.uri = uri
            return self

        def set_predicate(self, predicate: Predicate) -> Route.Builder:
            self.predicate = predicate
            return self

        def set_order(self, order: int) -> Route.Builder:
            self.order = order
            return self

        def set_metadata(self, metadata: {}) -> Route.Builder:
            self.metadata = metadata
            return self

        # TODO: and_predicate() is a function to call Predicate.and_predicate(),
        #  but it has not been implemented, and will be done in the future.
        #  Same situation to or_predicate() and negate_predicate()
        def and_predicate(self, predicate) -> Route.Builder:
            return self

        def or_predicate(self, predicate) -> Route.Builder:
            return self

        def negate_predicate(self) -> Route.Builder:
            return self

        def build(self) -> Route:
            not_none(self.route_id)
            not_none(self.uri)
            not_none(self.predicate)
            return Route(self.route_id, self.uri, self.order, self.predicate, self.gateway_filters, self.metadata)
