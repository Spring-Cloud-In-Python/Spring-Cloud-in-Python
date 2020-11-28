# -*- coding: utf-8 -*-
from __future__ import annotations

# standard library
from typing import List

__author__ = "Chaoyuuu (chaoyu2330@gmail.com)"
__license__ = "Apache 2.0"

# standard library
from abc import ABC, abstractmethod

# scip plugin
from spring_cloud.gateway.route import Route


class RouteLocator(ABC):
    @abstractmethod
    def get_routes(self) -> List[Route]:
        pass


class RouteLocatorBuilder:
    def routes(self) -> RouteLocatorBuilder.Builder:
        return self.Builder()

    class Builder:
        def __init__(self):
            self.__routes = []

        def route_with_id(self, route_id: str, f_) -> RouteLocatorBuilder.Builder:
            """
            Creates a new Route
            Args:
                route_id: the unique id for the route
                f_: a lambda function which takes in a PredicateSpec and returns a Route.Builder
            """
            # To solve the circular import between RouteSpec and RouteLocatorBuilder
            # scip plugin
            from spring_cloud.gateway.route.builder.spec import RouteSpec

            route_builder = f_(RouteSpec(self).id(route_id))
            self.__routes.append(route_builder)
            return self

        def route(self, f_) -> RouteLocatorBuilder.Builder:
            """
            Creates a new Route
            Args:
                f_: a lambda function which takes in a PredicateSpec and returns a Route.Builder
            """
            # To solve the circular import between RouteSpec and RouteLocatorBuilder
            # scip plugin
            from spring_cloud.gateway.route.builder.spec import RouteSpec

            route_builder = f_(RouteSpec(self).random_id())
            self.__routes.append(route_builder)
            return self

        def build(self) -> RouteLocator:
            self.__routes = [route_builder.build() for route_builder in self.__routes]
            return RouteLocator()

        def build_test(self) -> List[Route]:
            self.__routes = [route_builder.build() for route_builder in self.__routes]
            return self.__routes
