# -*- coding: utf-8 -*-
# standard library
from typing import List
from unittest.mock import Mock

# scip plugin
from spring_cloud.commons.helpers import NaiveCacheManager
from spring_cloud.gateway.route.definition import (
    CachingRouteDefinitionLocator,
    CompositeRouteDefinitionLocator,
    RouteDefinition,
    RouteDefinitionLocator,
    StaticRouteDefinitionLocator,
)

__author__ = "Waterball (johnny850807@gmail.com)"
__license__ = "Apache 2.0"


def definition(num):
    return RouteDefinition(str(num), [], [], f"uri-{num}")


class TestCompositeRouteDefinitionLocator:
    def test(self):
        # Use integers instead of actually constructing the RouteDefinitions
        locator1 = StaticRouteDefinitionLocator([definition(0), definition(1)])
        locator2 = StaticRouteDefinitionLocator([definition(2)])
        locator3 = StaticRouteDefinitionLocator([definition(3), definition(4), definition(5)])
        locator4 = StaticRouteDefinitionLocator([])

        composite = CompositeRouteDefinitionLocator([locator1, locator2, locator3, locator4])
        results: List[RouteDefinition] = composite.route_definitions

        for i in range(0, len(results)):
            assert results[i].id == str(i)
            assert results[i].uri == f"uri-{i}"


class TestCachingRouteDefinitionLocator:
    class Mock(RouteDefinitionLocator):
        """
        Mock for the property `route_definitions`
        """

        def __init__(self):
            self.call_count = 0

        @property
        def route_definitions(self) -> List[RouteDefinition]:
            self.call_count += 1
            return [definition(0)]

    def setup_class(self):
        self.delegate = TestCachingRouteDefinitionLocator.Mock()
        self.locator = CachingRouteDefinitionLocator(NaiveCacheManager(), self.delegate)

    def test_Given_cache_When_10_invocations_Then_only_1_cache_miss_and_delegate(self):
        for i in range(1, 10):
            results = self.locator.route_definitions
            assert len(results) == 1
            assert results[0].id == str(0)
            assert results[0].uri == "uri-0"
        assert self.delegate.call_count == 1
