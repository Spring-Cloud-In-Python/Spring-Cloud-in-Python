# -*- coding: utf-8 -*-
# standard library
from datetime import datetime
from unittest.mock import Mock

__author__ = "Chaoyuuu (chaoyu2330@gmail.com)"
__license__ = "Apache 2.0"

# scip plugin
from spring_cloud.gateway.handler.predicate.core import AfterRoutePredicate, CookieRoutePredicate, PathRoutePredicate
from spring_cloud.gateway.server import DefaultServerWebExchange, ServerHTTPResponse, StaticServerHttpRequest


class TestAfterRoutePredicate:
    def given_config_datetime(self, date_time: datetime):
        self.config = AfterRoutePredicate.Config(date_time)
        self.predicate = AfterRoutePredicate(self.config)

    def given_now(self, now: datetime):
        self.predicate.now_datetime_func = lambda: now

    def given_http_exchange(self):
        request = StaticServerHttpRequest()
        response_handler = Mock()
        response = ServerHTTPResponse(response_handler)
        self.exchange = DefaultServerWebExchange(request, response)

    def test_when_now_datatime_is_after_config_datetime_Then_return_T(self):
        self.given_config_datetime(datetime(2020, 11, 1))
        self.given_now(datetime(2020, 11, 11))
        self.given_http_exchange()
        assert self.predicate.test(self.exchange)

    def test_When_now_datetime_is_not_after_config_datetime_Then_return_F(self):
        self.given_config_datetime(datetime(2020, 12, 1))
        self.given_now(datetime(2020, 11, 11))
        self.given_http_exchange()
        assert not self.predicate.test(self.exchange)


class TestPathRoutePredicate:
    def given_config_pattern(self, pattern: str):
        self.config = PathRoutePredicate.Config(pattern)
        self.predicate = PathRoutePredicate(self.config)

    def given_http_request_url(self, url: str):
        request = StaticServerHttpRequest(url_=url)
        response_handler = Mock()
        response = ServerHTTPResponse(response_handler)
        self.exchange = DefaultServerWebExchange(request, response)

    def test_Given_path_When_match_pattern_Then_return_T(self):
        self.given_config_pattern("/api/users/**")
        self.given_http_request_url("http://localhost:8888/api/users/1")
        assert self.predicate.test(self.exchange)

    def test_Given_path_When_not_match_pattern_Then_return_F(self):
        self.given_config_pattern("/api/users/**")
        self.given_http_request_url("http://localhost:8888/api/messages")
        assert not self.predicate.test(self.exchange)


class TestCookieRoutePredicate:
    def given_config_cookie(self, cookie_name, cookie_value):
        self.config = CookieRoutePredicate.Config(cookie_name, cookie_value)
        self.predicate = CookieRoutePredicate(self.config)

    def give_http_cookies(self, cookies={}):
        request = StaticServerHttpRequest(cookies=cookies)
        response_handler = Mock()
        response = ServerHTTPResponse(response_handler)
        self.exchange = DefaultServerWebExchange(request, response)

    def test_Given_cookies_from_config_When_match_cookie_Then_return_T(self):
        self.given_config_cookie("my_cookie", "ch.p")
        self.give_http_cookies({"your_cookie": "sugar", "my_cookie": "ch.p"})
        assert self.predicate.test(self.exchange)

    def test_Given_cookies_from_config_When_not_match_cookie_Then_return_F(self):
        self.given_config_cookie("my_cookie", "ch.p")
        self.give_http_cookies({"your_cookie": "sugar", "his_cookie": "chocolate"})
        assert not self.predicate.test(self.exchange)

    def test_Given_cookies_from_config_in_regex_When_match_cookie_Then_return_T(self):
        self.given_config_cookie("my_cookie", r"chocolate[0-9]+")
        self.give_http_cookies({"your_cookie": "sugar", "my_cookie": "chocolate123"})
        assert self.predicate.test(self.exchange)

    def test_Given_cookies_from_config_in_regex_When_not_match_cookie_Then_return_F(self):
        self.given_config_cookie("my_cookie", r"chocolate[0-9]+")
        self.give_http_cookies({"your_cookie": "sugar", "his_cookie": "chocolate"})
        assert not self.predicate.test(self.exchange)

    def test_Given_no_cookies_from_exchange_When_test_Should_be_F(self):
        self.given_config_cookie("my_cookie", "ch.p")
        self.give_http_cookies()
        assert not self.predicate.test(self.exchange)
