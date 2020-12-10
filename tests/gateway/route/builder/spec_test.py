# -*- coding: utf-8 -*-

__author__ = "Chaoyuuu (chaoyu2330@gmail.com)"
__license__ = "Apache 2.0"

# standard library
from datetime import datetime

# scip plugin
from spring_cloud.gateway.handler.predicate.core import AfterRoutePredicate, CookieRoutePredicate, PathRoutePredicate
from spring_cloud.gateway.handler.predicate.operator_gateway_predicate import (
    AndGatewayPredicate,
    NegateGatewayPredicate,
    OrGatewayPredicate,
)
from spring_cloud.gateway.route import Route
from spring_cloud.gateway.route.builder.route_locator import RouteLocatorBuilder
from spring_cloud.gateway.route.builder.spec import PredicateSpec


class TestRouteBuilder:
    def given_predicate_spec_and_gateway_filter_spec(self):
        self.route_builder = Route.Builder()
        self.builder = RouteLocatorBuilder.Builder()
        self.p = PredicateSpec(self.route_builder, self.builder)

    def test_basic_route_builder(self):
        self.given_predicate_spec_and_gateway_filter_spec()
        route_builder = (
            self.p.path("/get").filters(lambda f: f.add_request_header("Hello", "Johnny")).uri("http://a_cat")
        )
        assert isinstance(route_builder, Route.Builder)

    def test_route_builder_with_logical_operator(self):
        self.given_predicate_spec_and_gateway_filter_spec()
        route_builder = (
            self.p.path("/andnotquery")
            .and_()
            .not_(lambda p: p.after(datetime(2020, 11, 11)))
            .filters(lambda f: f.add_request_header("Hello", "Johnny"))
            .uri("http://a_cat")
        )
        assert isinstance(route_builder, Route.Builder)


class TestPredicateSyntaxTreeInRoutes:
    def given_route_locator(self):
        builder = RouteLocatorBuilder()
        self.route_locator = (
            builder.routes()
            .route(lambda p: p.path("/get").and_().not_(lambda d: d.cookie("key", "value")).uri("http://a_cat"))
            .route(
                lambda p: p.path("/get")
                .or_()
                .cookie("key", "value")
                .and_()
                .after(datetime(2020, 11, 11))
                .uri("http://a_cat")
            )
            .build()
        )

    def test_predicate_syntax_tree_should_match(self):
        self.given_route_locator()
        routes = self.route_locator.get_routes()
        route_predicate_0 = routes[0].predicate
        assert isinstance(route_predicate_0, AndGatewayPredicate)
        assert isinstance(route_predicate_0.left, PathRoutePredicate)
        assert isinstance(route_predicate_0.right, NegateGatewayPredicate)
        assert isinstance(route_predicate_0.right.p, CookieRoutePredicate)

        route_predicate_1 = routes[1].predicate
        assert isinstance(route_predicate_1, AndGatewayPredicate)
        assert isinstance(route_predicate_1.left, OrGatewayPredicate)
        assert isinstance(route_predicate_1.right, AfterRoutePredicate)
        assert isinstance(route_predicate_1.left.left, PathRoutePredicate)
        assert isinstance(route_predicate_1.left.right, CookieRoutePredicate)
