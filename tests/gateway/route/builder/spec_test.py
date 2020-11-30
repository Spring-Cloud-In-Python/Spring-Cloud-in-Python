# -*- coding: utf-8 -*-

__author__ = "Chaoyuuu (chaoyu2330@gmail.com)"
__license__ = "Apache 2.0"

# standard library
from datetime import datetime

# scip plugin
from spring_cloud.gateway.route import Route
from spring_cloud.gateway.route.builder.route_locator import RouteLocatorBuilder
from spring_cloud.gateway.route.builder.spec import PredicateSpec


class TestSpec:
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
