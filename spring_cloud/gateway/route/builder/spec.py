# -*- coding: utf-8 -*-
from __future__ import annotations

# standard library
import re
import uuid
from datetime import datetime
from enum import Enum
from typing import Callable, List, TypeVar

__author__ = "Chaoyuuu (chaoyu2330@gmail.com)"
__license__ = "Apache 2.0"

# standard library
from abc import ABC

# scip plugin
from spring_cloud.gateway.filter import GatewayFilter
from spring_cloud.gateway.filter.factory.core import (
    AddRequestHeaderGatewayFilterFactory,
    AddResponseHeaderGatewayFilterFactory,
    NameValueConfig,
    PrefixPathGatewayFilterFactory,
)
from spring_cloud.gateway.handler.predicate import NOT, Predicate
from spring_cloud.gateway.handler.predicate.core import (
    AfterRoutePredicate,
    AfterRoutePredicateFactory,
    CookieRoutePredicate,
    CookieRoutePredicateFactory,
    PathRoutePredicate,
    PathRoutePredicateFactory,
)
from spring_cloud.gateway.route import Route
from spring_cloud.gateway.route.builder.route_locator import RouteLocatorBuilder
from spring_cloud.utils.validate import not_none

Datetime = TypeVar("Datetime", bound=datetime)


class UriSpec(ABC):
    """
     A specification to add a URI to a route.
    """

    def __init__(self, route_builder: Route.Builder, builder: RouteLocatorBuilder.Builder):
        self.route_builder = route_builder
        self.builder = builder

    def metadata(self, key: str, value: object) -> UriSpec:
        self.route_builder.set_metadata(key, value)
        return self

    def uri(self, uri: str) -> Route.Builder:
        return self.route_builder.set_uri(uri)


class PredicateSpec(UriSpec):
    def __init__(self, route_builder: Route.Builder, builder: RouteLocatorBuilder.Builder):
        super().__init__(route_builder, builder)

    def order(self, order: int) -> PredicateSpec:
        self.route_builder.set_order(order)
        return self

    def predicate(self, predicate: Predicate) -> BooleanSpec:
        self.route_builder.set_predicate(predicate)
        return BooleanSpec(self.route_builder, self.builder)

    def create_gateway_predicate_spec(self) -> GatewayFilterSpec:
        return GatewayFilterSpec(self.route_builder, self.builder)

    def after(self, date_time: Datetime) -> BooleanSpec:
        """
        A predicate to check if a request was made after a specific {@link ZonedDateTime}.
        Args:
            date_time: requests would only be routed after this {@link ZonedDateTime}

        Returns: return a BooleanSpec to be used to add logical operators
        """
        config = AfterRoutePredicate.Config(date_time)
        return self.predicate(AfterRoutePredicateFactory().apply(config))

    def path(self, patterns: str) -> BooleanSpec:
        """
        A predicate that checks if the path of the request matches the given pattern.
        Args:
            patterns: the pattern to check the path against.

        Returns: return a BooleanSpec to be used to add logical operators
        """
        config = PathRoutePredicate.Config(patterns)
        return self.predicate(PathRoutePredicateFactory().apply(config))

    def cookie(self, name: str, value: str) -> BooleanSpec:
        """
         A predicate that checks if a cookie matches a given regular expression.
        Args:
            name: th name of the cookie
            value: the value of the cookies will be evaluated against this regular expression

        Returns: return a BooleanSpec to be used to add logical operators
        """
        config = CookieRoutePredicate.Config(name, value)
        return self.predicate(CookieRoutePredicateFactory().apply(config))


class Operator(Enum):
    AND = "AND"
    OR = "OR"
    NEGATE = "NEGATE"


class BooleanSpec(UriSpec):
    """
    A spec used to apply logical operators.
    """

    def __init__(self, route_builder: Route.Builder, builder: RouteLocatorBuilder.Builder):
        super().__init__(route_builder, builder)
        self.predicate = route_builder.predicate

    def and_(self) -> BooleanOpSpec:
        return self.BooleanOpSpec(self.route_builder, self.builder, Operator.AND)

    def or_(self) -> BooleanOpSpec:
        return self.BooleanOpSpec(self.route_builder, self.builder, Operator.OR)

    def negate_(self) -> BooleanSpec:
        self.route_builder.negate_()
        return BooleanSpec(self.route_builder, self.builder)

    def filters(self, f_: Callable[[GatewayFilterSpec], UriSpec]) -> UriSpec:
        """
        Args:
            f_: lambda: GatewayFilterSpec -> UriSpec
        """
        return f_(GatewayFilterSpec(self.route_builder, self.builder))

    class BooleanOpSpec(PredicateSpec):
        def __init__(self, route_builder: Route.Builder, builder: RouteLocatorBuilder.Builder, operator: Operator):
            super().__init__(route_builder, builder)
            self.operator = operator

        def predicate(self, predicate: Predicate) -> BooleanSpec:

            not_none(self.operator)
            if self.operator == Operator.AND:
                self.route_builder.and_(predicate)
            elif self.operator == Operator.OR:
                self.route_builder.or_(predicate)
            elif self.operator == Operator.NEGATE:
                self.route_builder.negate_()
            return BooleanSpec(self.route_builder, self.builder)

        def not_(self, p_: Callable[[PredicateSpec], BooleanSpec]) -> BooleanSpec:
            """
            Args:
                p_: lambda: PredicateSpec -> BooleanSpec
            """
            return p_(BooleanSpec.NotOpSpec(self.route_builder, self.builder, self.operator))

    class NotOpSpec(BooleanOpSpec):
        def __init__(self, route_builder: Route.Builder, builder: RouteLocatorBuilder.Builder, operator: Operator):
            super().__init__(route_builder, builder, operator)

        def predicate(self, predicate) -> BooleanSpec:
            negated = NOT(predicate)
            return super().predicate(negated)


class GatewayFilterSpec(UriSpec):
    """
    Applies specific filters to routes.
    """

    def __init__(self, route_builder: Route.Builder, builder: RouteLocatorBuilder.Builder):
        super().__init__(route_builder, builder)

    def filters(self, gateway_filters: List) -> GatewayFilterSpec:
        """
        Applies the list of filters to the route.
        Args:
            gateway_filters: the filters to apply

        Returns: a GatewayFilterSpec that can be used to apply additional filters
        """
        self.route_builder.filters(gateway_filters)
        return self

    def filter(self, gateway_filter: GatewayFilter) -> GatewayFilterSpec:
        """
        Applies the filter to the route.
        Args:
            gateway_filter: the filters to apply

        Returns: a GatewayFilterSpec that can be used to apply additional filters
        """
        self.route_builder.filter(gateway_filter)
        return self

    def add_request_header(self, header_name: str, header_value: str) -> GatewayFilterSpec:
        """
        Add a request header to the request before it is routed by the Gateway.
        Args:
            header_name: the header name
            header_value: the header value

        Returns: a GatewayFilterSpec that can be used to apply additional filters
        """
        config = NameValueConfig(header_name, header_value)
        return self.filter(AddRequestHeaderGatewayFilterFactory().apply(config))

    def add_response_header(self, header_name: str, header_value: str) -> GatewayFilterSpec:
        """
        Adds a header to the response returned to the Gateway from the route.
        Args:
            header_name: the header name
            header_value: the header value

        Returns: a GatewayFilterSpec that can be used to apply additional filters
        """
        config = NameValueConfig(header_name, header_value)
        return self.filter(AddResponseHeaderGatewayFilterFactory().apply(config))

    def prefix_path(self, prefix: str) -> GatewayFilterSpec:
        config = PathRoutePredicate.Config(prefix)
        return self.filter(PrefixPathGatewayFilterFactory().apply(config))


class RouteSpec:
    def __init__(self, builder: RouteLocatorBuilder.Builder):
        self.__builder = builder
        self.__route_builder = Route.Builder()

    def id(self, route_id: str) -> PredicateSpec:
        self.__route_builder.set_route_id(route_id)
        return self.predicate_builder()

    def random_id(self) -> PredicateSpec:
        self.__route_builder.set_route_id(str(uuid.uuid4()))
        return self.predicate_builder()

    def predicate_builder(self) -> PredicateSpec:
        return PredicateSpec(self.__route_builder, self.__builder)
