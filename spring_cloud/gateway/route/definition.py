# -*- coding: utf-8 -*-
# standard library
import uuid
from abc import ABC, abstractmethod
from typing import List

# scip plugin
from spring_cloud.commons.helpers import CacheManager
from spring_cloud.utils.functional_operators import flat_map

__author__ = "Waterball (johnny850807@gmail.com)"
__license__ = "Apache 2.0"


class FilterDefinition:
    def __init__(self, name: str, **kwargs):
        self.name = name
        self.args = kwargs


class PredicateDefinition:
    def __init__(self, name: str, **kwargs):
        self.name = name
        self.args = kwargs


class RouteDefinition:
    def __init__(
        self,
        id_: str,
        predicates: List[PredicateDefinition],
        filters: List[FilterDefinition],
        uri: str,
        order: int = 0,
        **kwargs
    ):
        self.id = id_
        self.predicates = predicates
        self.filters = filters
        self.uri = uri
        self.metadata = kwargs
        self.order = order


class RouteDefinitionLocator(ABC):
    @property
    @abstractmethod
    def route_definitions(self) -> List[RouteDefinition]:
        raise NotImplemented


class StaticRouteDefinitionLocator(RouteDefinitionLocator):
    def __init__(self, definitions: List[RouteDefinition]):
        self.definitions = definitions

    @property
    def route_definitions(self) -> List[RouteDefinition]:
        return self.definitions


class CompositeRouteDefinitionLocator(RouteDefinitionLocator):
    def __init__(self, locators: List[RouteDefinitionLocator]):
        self.locators = locators

    @property
    def route_definitions(self) -> List[RouteDefinition]:
        definitions = flat_map(lambda l: l.route_definitions, self.locators)
        for definition in definitions:
            definition.id = definition.id or self.__random_id()
        return definitions

    @staticmethod
    def __random_id():
        return uuid.uuid1()


class CachingRouteDefinitionLocator(RouteDefinitionLocator):
    CACHE_NAME = "CachingRouteDefinitionLocator/CacheKey"

    def __init__(self, cache_manager: CacheManager, delegate: RouteDefinitionLocator):
        self.delegate = delegate
        self.__cache_manager = cache_manager

    @property
    def route_definitions(self) -> List[RouteDefinition]:
        return self.__cache_manager.get(self.CACHE_NAME).on_cache_miss(lambda: self.delegate.route_definitions)
