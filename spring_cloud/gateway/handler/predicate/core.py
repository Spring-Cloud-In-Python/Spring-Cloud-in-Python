# -*- coding: utf-8 -*-
from __future__ import annotations

# standard library
import re
from datetime import datetime

__author__ = "Chaoyuuu (chaoyu2330@gmail.com)"
__license__ = "Apache 2.0"

# scip plugin
from spring_cloud.gateway.handler.predicate import Predicate
from spring_cloud.gateway.handler.predicate.base import RoutePredicateFactory
from spring_cloud.gateway.pathpattern import PathPatternParser
from spring_cloud.gateway.server import ServerWebExchange


class AfterRoutePredicateFactory(RoutePredicateFactory):
    def apply(self, config) -> Predicate:
        return AfterRoutePredicate(config)


class PathRoutePredicateFactory(RoutePredicateFactory):
    def apply(self, config) -> Predicate:
        return PathRoutePredicate(config)


class CookieRoutePredicateFactory(RoutePredicateFactory):
    def apply(self, config) -> Predicate:
        return CookieRoutePredicate(config)


class AfterRoutePredicate(Predicate):
    def __init__(self, config: AfterRoutePredicate.Config, now_datetime_func=None):
        self.now_datetime_func = now_datetime_func
        self.config = config

    def test(self, exchange: ServerWebExchange) -> bool:
        now = self.now_datetime_func() if self.now_datetime_func else datetime.now()
        return now > self.config.date_time

    class Config:
        def __init__(self, date_time: datetime):
            self.date_time = date_time


class PathRoutePredicate(Predicate):
    def __init__(self, config: PathRoutePredicate.Config):
        self.config = config

    def test(self, exchange: ServerWebExchange) -> bool:
        request_path = exchange.request.path
        path_pattern = PathPatternParser.parse(self.config.pattern)
        return path_pattern.matches(request_path)

    class Config:
        def __init__(self, pattern=None):
            self.pattern = pattern


class CookieRoutePredicate(Predicate):
    def __init__(self, config: CookieRoutePredicate.Config):
        self.config = config

    def test(self, exchange: ServerWebExchange) -> bool:
        http_request_cookies = exchange.request.cookies
        for key, value in http_request_cookies.items():
            if self.__match_cookie(key, value):
                return True
        return False

    def __match_cookie(self, key: str, value: str):
        return re.match(self.config.cookie_name, key) and re.match(self.config.cookie_regexp, value)

    class Config:
        def __init__(self, cookie_name=None, cookie_regexp=None):
            self.cookie_name = cookie_name
            self.cookie_regexp = cookie_regexp
