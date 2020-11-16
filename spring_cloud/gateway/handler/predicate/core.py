# -*- coding: utf-8 -*-
# standard library
import re
from datetime import datetime

__author__ = "Chaoyuuu (chaoyu2330@gmail.com)"
__license__ = "Apache 2.0"

# scip plugin
from spring_cloud.gateway.handler.predicate.base import RoutePredicateFactory
from spring_cloud.gateway.handler.predicate.predicate import Predicate


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
        def __init__(self):
            self.date_time = None


class PathRoutePredicate(Predicate):
    def __init__(self, config):
        self.config = config

    def test(self, http_request) -> bool:
        path_patterns = http_request
        return self.config.pattern in path_patterns

    class Config:
        def __init__(self):
            self.pattern = None


class CookieRoutePredicate(Predicate):
    def __init__(self, config):
        self.config = config

    # TODO: the cookies is dependency with http_request, but we haven't decided the tool,
    #  that is, the type of the cookies may be change in future
    def test(self, http_request) -> bool:
        http_request_cookies = http_request
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
        def __init__(self):
            self.cookie_name = None
            self.cookie_value = None
