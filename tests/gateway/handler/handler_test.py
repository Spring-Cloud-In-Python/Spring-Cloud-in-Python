# -*- coding: utf-8 -*-

__author__ = "Chaoyuuu (chaoyu2330@gmail.com)"
__license__ = "Apache 2.0"

# standard library
from unittest.mock import Mock

# scip plugin
from spring_cloud.gateway.handler.handler import RoutePredicateHandlerMapping
from spring_cloud.gateway.route.builder.route_locator import RouteLocatorBuilder
from spring_cloud.gateway.server import DefaultServerWebExchange, ServerHTTPResponse, StaticServerHttpRequest


class TestRoutePredicateHandlerMapping:
    def given_routes_with_path_predicate(self, path1: str, path2: str):
        builder = RouteLocatorBuilder()
        route_locator = (
            builder.routes()
            .route(lambda p: p.path(path1).uri("http://a_cat"), "route1")
            .route(lambda p: p.path(path2).uri("http://a_dog"), "route2")
            .build()
        )
        filtering_web_handler = Mock()
        self.predicate_handler = RoutePredicateHandlerMapping(route_locator)

    def given_http_request(self, url: str):
        request = StaticServerHttpRequest(url_=url)
        handler = Mock()
        response = ServerHTTPResponse(handler)
        self.exchange = DefaultServerWebExchange(request, response)

    def test_Given_routes_with_path_predicate_When_lookup_route_Then_return_matched_route(self):
        self.given_routes_with_path_predicate(path1="/users", path2="/api/users/**")
        self.given_http_request("http://localhost:8888/api/users/1")
        route = self.predicate_handler.lookup_route(self.exchange)
        assert route.route_id == "route2"

    def test_Given_routes_with_no_matched_When_lookup_route_Then_return_None(self):
        self.given_routes_with_path_predicate(path1="/users", path2="/api")
        self.given_http_request("http://localhost:8888/api/users/1")
        route = self.predicate_handler.lookup_route(self.exchange)
        assert route is None

    def test_Given_routes_both_matched_the_predicate_When_lookup_route_Then_return_the_first_matched_route(self):
        self.given_routes_with_path_predicate(path1="/api/users/1", path2="/api/users/1")
        self.given_http_request("http://localhost:8888/api/users/1")
        route = self.predicate_handler.lookup_route(self.exchange)
        assert route.route_id == "route1"
