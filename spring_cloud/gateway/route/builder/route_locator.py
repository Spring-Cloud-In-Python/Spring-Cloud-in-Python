# -*- coding: utf-8 -*-
from __future__ import annotations

# standard library
from abc import ABC, abstractmethod
from typing import List

__author__ = "Chaoyuuu (chaoyu2330@gmail.com)"
__license__ = "Apache 2.0"

# scip plugin
from spring_cloud.commons.helpers import CacheManager
from spring_cloud.gateway.route import Route
from spring_cloud.utils.functional_operators import flat_map


class RouteLocator(ABC):
    @abstractmethod
    def get_routes(self) -> List[Route]:
        pass


class StaticRouteLocator(RouteLocator):
    def __init__(self, routes: List[Route]):
        self.routes = routes

    def get_routes(self) -> List[Route]:
        return self.routes


class CompositeRouteLocator(RouteLocator):
    def __init__(self, delegates: List[RouteLocator]):
        self.delegates = delegates

    def get_routes(self) -> List[Route]:
        return flat_map(lambda r: r.get_routes(), self.delegates)


class CachingRouteLocator(RouteLocator):
    CACHE_NAME = "CachingRouteLocator/CacheKey"

    def __init__(self, cache_manager: CacheManager, delegate: RouteLocator):
        self.delegate = delegate
        self.__cache_manager = cache_manager

    def get_routes(self) -> List[Route]:
        return self.__cache_manager.get(self.CACHE_NAME).on_cache_miss(lambda: self.delegate.get_routes())


class RouteLocatorBuilder:
    def routes(self) -> RouteLocatorBuilder.Builder:
        return self.Builder()

    class Builder:
        def __init__(self):
            self.__route_builders = []

        def route(self, f_, route_id: str = None) -> RouteLocatorBuilder.Builder:
            """
            Creates a new Route
            Args:
                route_id: the unique id for the route
                f_: a lambda function which takes in a PredicateSpec and returns a Route.Builder
            """
            # To solve the circular import between RouteSpec and RouteLocatorBuilder
            # scip plugin
            from spring_cloud.gateway.route.builder.spec import RouteSpec

            if route_id:
                route_builder = f_(RouteSpec(self).id(route_id))
            else:
                route_builder = f_(RouteSpec(self).random_id())

            self.__route_builders.append(route_builder)
            return self

        def build(self) -> RouteLocator:
            return StaticRouteLocator([route_builder.build() for route_builder in self.__route_builders])
