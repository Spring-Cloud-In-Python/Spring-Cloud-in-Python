# -*- coding: utf-8 -*-
# standard library
from typing import List, Optional

__author__ = "Chaoyuuu (chaoyu2330@gmail.com)"
__license__ = "Apache 2.0"

# scip plugin
from spring_cloud.gateway.filter import GatewayFilter, GatewayFilterChain, GlobalFilter
from spring_cloud.gateway.route import Route
from spring_cloud.gateway.route.builder.route_locator import RouteLocator
from spring_cloud.gateway.server import (
    GATEWAY_HANDLER_MAPPER_ATTR,
    GATEWAY_PREDICATE_ROUTE_ATTR,
    GATEWAY_ROUTE_ATTR,
    ServerWebExchange,
)
from spring_cloud.utils.functional_operators import filter_get_first
from spring_cloud.utils.logging import getLogger


class FilteringWebHandler:
    def __init__(self, global_filters: List[GlobalFilter]):
        self.__global_filters = self.load_filters(global_filters)

    def load_filters(self, global_filters: List[GlobalFilter]):
        return [GatewayFilterAdapter(global_filter) for global_filter in global_filters]

    # TODO: gateway_filters must be sorted by order
    def handle(self, exchange: ServerWebExchange) -> None:
        route: Route = exchange.attributes[GATEWAY_ROUTE_ATTR]
        gateway_filters = route.filters
        gateway_filters.extend(self.__global_filters)
        return DefaultGatewayFilterChain(gateway_filters).filter(exchange)


class GatewayFilterAdapter(GatewayFilter):
    def __init__(self, delegate: GlobalFilter):
        self.__delegate = delegate

    def filter(self, exchange: ServerWebExchange, chain: GatewayFilterChain) -> None:
        return self.__delegate.filter(exchange, chain)


class DefaultGatewayFilterChain(GatewayFilterChain):
    def __init__(self, filters: List[GatewayFilter], index=None):
        self.__index = index or 0
        self.__gateway_filters = filters

    @staticmethod
    def create(gateway_filters: List[GatewayFilter], index: int):
        return DefaultGatewayFilterChain(gateway_filters, index)

    def filter(self, exchange: ServerWebExchange) -> None:
        """
        Traverse filters
        """
        if self.__index < len(self.__gateway_filters):
            gateway_filter = self.__gateway_filters[self.__index]
            chain = self.create(self.__gateway_filters, self.__index + 1)
            return gateway_filter.filter(exchange, chain)
        else:
            return None


class RoutePredicateHandlerMapping:
    def __init__(self, web_handler: FilteringWebHandler, route_locator: RouteLocator):
        self.__web_handler = web_handler
        self.__route_locator = route_locator
        self.logger = getLogger(name="spring_cloud_gateway.RoutePredicateHandlerMapping", debug=True)

    def get_handler(self, exchange: ServerWebExchange) -> Optional[FilteringWebHandler]:
        """
        Test routes' predicate and pass the matched Route to FilteringWebHandler by exchange's attribute
        Returns: FilteringWebHandler, this is for DispatchHandler to continue the fluent flow.
        """
        exchange.attributes[GATEWAY_HANDLER_MAPPER_ATTR] = "RoutePredicateHandlerMapping"
        route = self.lookup_route(exchange)
        exchange.attributes.pop(GATEWAY_PREDICATE_ROUTE_ATTR, None)
        self.logger.debug(f"Mapping [{self.get_exchange_desc(exchange)}] to {route}")
        exchange.attributes[GATEWAY_ROUTE_ATTR] = route

        if route is None:
            return None
        return self.__web_handler

    def lookup_route(self, exchange: ServerWebExchange) -> Optional[Route]:
        """
        Testing each route's predicate, and return the first item that satisfy the request.
        if here is no matched route, return None
        """
        routes = self.__route_locator.get_routes()
        route = filter_get_first(lambda route: route.predicate.test(exchange), routes)

        if route:
            self.logger.info(f"Route matched: {route.route_id}")
            return route
        else:
            self.logger.info(f"No route matched.")
            return None

    # TODO: return exchange.request information for debug
    def get_exchange_desc(self, exchange: ServerWebExchange):
        return f"Exchange: exchange.request.get_method() exchange.request.get_method()"


class DispatcherHandler:
    def __init__(self):
        pass

    # TODO: Implement RoutePredicateHandlerMapping and FilteringWebHandler
    def handle(self, exchange: ServerWebExchange):
        pass
