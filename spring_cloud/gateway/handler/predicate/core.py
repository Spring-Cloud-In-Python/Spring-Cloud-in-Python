# -*- coding: utf-8 -*-
# standard library
import re
from datetime import datetime

__author__ = "Chaoyuuu (chaoyu2330@gmail.com)"
__license__ = "Apache 2.0"

# scip plugin
from spring_cloud.gateway.handler.predicate import Predicate
from spring_cloud.gateway.handler.predicate.base import RoutePredicateFactory


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
    def __init__(self, config, now_datetime_func=None):
        self.now_datetime_func = now_datetime_func
        self.config = config

    def test(self, http_request) -> bool:
        now = self.now_datetime_func() if self.now_datetime_func else datetime.now()
        return now > self.config.date_time

    class Config:
        def __init__(self, date_time: datetime):
            self.date_time = date_time


# TODO: Implement ant pattern matching
class PathRoutePredicate(Predicate):
    def __init__(self, config):
        self.config = config

    def test(self, http_request) -> bool:
        path_patterns = http_request.path_patterns
        return self.config.pattern in path_patterns

    class Config:
        def __init__(self, pattern=None):
            self.pattern = pattern


class CookieRoutePredicate(Predicate):
    def __init__(self, config):
        self.config = config

    def test(self, http_request) -> bool:
        http_request_cookies = http_request.cookies

        if http_request_cookies is None:
            return False

        for cookie_name in http_request_cookies:
            if re.match(self.config.cookie_name, cookie_name):
                values = http_request_cookies[cookie_name]
                for value in values:
                    if re.match(self.config.cookie_value, value):
                        return True
        return False

    class Config:
        def __init__(self, cookie_name=None, cookie_value=None):
            self.cookie_name = cookie_name
            self.cookie_value = cookie_value
