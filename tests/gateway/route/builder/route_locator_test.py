# -*- coding: utf-8 -*-

__author__ = "Chaoyuuu (chaoyu2330@gmail.com)"
__license__ = "Apache 2.0"

# standard library
from datetime import datetime

# scip plugin
from spring_cloud.gateway.route.builder.route_locator import RouteLocatorBuilder


class TestRouteLocatorBuilder:
    def given_route_locator_builder(self):
        self.builder = RouteLocatorBuilder()

    def test_basic_route(self):
        self.given_route_locator_builder()
        routes = (
            self.builder.routes()
            .route(
                lambda p: p.path("/get").filters(lambda f: f.add_request_header("Hello", "Johnny")).uri("http://a_cat")
            )
            .build_test()
        )

        route = routes[0]
        assert len(routes) == 1
        assert route.uri == "http://a_cat"

    def test_routes_with_logical_opertor(self):
        self.given_route_locator_builder()
        routes = (
            self.builder.routes()
            .route_with_id(
                "test1",
                lambda p: p.path("/andnotquery")
                .and_()
                .not_(lambda p: p.after(datetime(2020, 11, 11)))
                .filters(lambda f: f.add_request_header("Hello", "Johnny"))
                .uri("http://a_cat"),
            )
            .route(
                lambda p: p.cookie("cookie", "chocolate")
                .filters(lambda f: f.add_response_header("Hello", "TsengMJ").add_request_header("Ha", "Haribo"))
                .metadata("A", "Apple")
                .uri("http://a_dog")
            )
            .build_test()
        )

        assert len(routes) == 2
        route_1 = routes[0]
        assert route_1.route_id == "test1"
        assert len(route_1.filter) == 1
        assert route_1.uri == "http://a_cat"
        route_2 = routes[1]
        assert len(route_2.filter) == 2
        assert route_2.uri == "http://a_dog"
        assert route_2.metadata["A"] == "Apple"
