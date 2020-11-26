# -*- coding: utf-8 -*-

__author__ = "Chaoyuuu (chaoyu2330@gmail.com)"
__license__ = "Apache 2.0"

# standard library
from datetime import datetime

# scip plugin
from spring_cloud.gateway.handler.predicate import TRUE
from spring_cloud.gateway.route import Route
from spring_cloud.gateway.route.builder.spec import GatewayFilterSpec, PredicateSpec


class TestGatewayFilterSpec:
    def give_gateway_filter_spec(self):
        self.route_builder = Route.Builder().set_route_id(1).set_uri("http://a_cat").set_predicate(TRUE)
        self.builder = None
        self.gateway_filter_spec = GatewayFilterSpec(self.route_builder, self.builder)

    def test_Given_NameValueConfig_when_add_request_header(self):
        self.give_gateway_filter_spec()
        gateway_filter_spec_test = self.gateway_filter_spec.add_request_header("hello", "world")
        assert isinstance(gateway_filter_spec_test, GatewayFilterSpec)


class TestSpec:
    def give_predicate_spec(self):
        self.route_builder = Route.Builder().set_route_id(1).set_uri("http://a_cat").set_predicate(TRUE)
        self.builder = None
        self.p = PredicateSpec(self.route_builder, self.builder)
        self.f = GatewayFilterSpec(self.route_builder, self.builder)

    def test_syntactic_sugar(self):
        self.give_predicate_spec()
        syntactic_sugar = (
            self.p.path("/get").filters(lambda f: f.add_request_header("Hello", "Johnny")).uri("http://a_cat")
        )
        assert isinstance(syntactic_sugar, Route.Builder)

    def test_syntactic_sugar_with_logical_operator(self):
        self.give_predicate_spec()
        syntactic_sugar = (
            self.p.path("/andnotquery")
            .and_spec()
            .not_spec(lambda p: p.after(datetime(2020, 11, 11)))
            .filters(lambda f: f.add_request_header("Hello", "Johnny"))
            .uri("http://a_cat")
        )
        assert isinstance(syntactic_sugar, Route.Builder)
