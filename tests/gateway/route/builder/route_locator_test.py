# -*- coding: utf-8 -*-

__author__ = "Chaoyuuu (chaoyu2330@gmail.com)"
__license__ = "Apache 2.0"

# standard library
from datetime import datetime
from typing import List

# scip plugin
from spring_cloud.commons.helpers import NaiveCacheManager
from spring_cloud.gateway.handler.predicate import TRUE
from spring_cloud.gateway.route import Route
from spring_cloud.gateway.route.builder.route_locator import (
    CachingRouteLocator,
    CompositeRouteLocator,
    RouteLocator,
    RouteLocatorBuilder,
    StaticRouteLocator,
)


def route(num):
    builder = Route.Builder()
    return builder.set_uri(f"uri-{num}").set_predicate(TRUE).set_route_id(num).build()


class TestCompositeRouteLocator:
    def test(self):
        # Use integers instead of actually constructing the Routes
        locator1 = StaticRouteLocator([route(1), route(2)])
        locator2 = StaticRouteLocator([route(3)])
        locator3 = StaticRouteLocator([route(4), route(5), route(6)])
        locator4 = StaticRouteLocator([])

        composite = CompositeRouteLocator([locator1, locator2, locator3, locator4])
        results: List[Route] = composite.get_routes()

        for i in range(0, len(results)):
            assert results[i].route_id == i + 1
            assert results[i].uri == f"uri-{i + 1}"


class TestCachingRouteLocator:
    class Mock(RouteLocator):
        """
        Mock for the property `routes`
        """

        def __init__(self):
            self.call_count = 0

        def get_routes(self) -> List[Route]:
            self.call_count += 1
            return [route(1)]

    def setup_class(self):
        self.delegate = TestCachingRouteLocator.Mock()
        self.locator = CachingRouteLocator(NaiveCacheManager(), self.delegate)

    def test_Given_cache_When_10_invocations_Then_only_1_cache_miss_and_delegate(self):
        for i in range(1, 10):
            results = self.locator.get_routes()
            assert len(results) == 1
            assert results[0].route_id == 1
            assert results[0].uri == "uri-1"
        assert self.delegate.call_count == 1


class TestRouteLocatorBuilder:
    def given_route_locator_builder(self):
        self.builder = RouteLocatorBuilder()

    def test_basic_route(self):
        self.given_route_locator_builder()
        route_locator = (
            self.builder.routes()
            .route(
                lambda p: p.path("/get").filters(lambda f: f.add_request_header("Hello", "Johnny")).uri("http://a_cat")
            )
            .build()
        )

        routes = route_locator.get_routes()
        assert len(routes) == 1
        assert routes[0].uri == "http://a_cat"

    def test_routes_with_logical_opertor(self):
        self.given_route_locator_builder()
        route_locator = (
            self.builder.routes()
            .route(
                lambda p: p.path("/andnotquery")
                .and_()
                .not_(lambda p: p.after(datetime(2020, 11, 11)))
                .filters(lambda f: f.add_request_header("Hello", "Johnny"))
                .uri("http://a_cat"),
                "test1",
            )
            .route(
                lambda p: p.cookie("cookie", "chocolate")
                .filters(lambda f: f.add_response_header("Hello", "TsengMJ").add_request_header("Ha", "Haribo"))
                .metadata("A", "Apple")
                .uri("http://a_dog")
            )
            .build()
        )

        routes = route_locator.get_routes()
        assert len(routes) == 2
        route_0 = routes[0]
        assert route_0.route_id == "test1"
        assert len(route_0.filters) == 1
        assert route_0.uri == "http://a_cat"

        route_1 = routes[1]
        assert len(route_1.filters) == 2
        assert route_1.uri == "http://a_dog"
        assert route_1.metadata["A"] == "Apple"
