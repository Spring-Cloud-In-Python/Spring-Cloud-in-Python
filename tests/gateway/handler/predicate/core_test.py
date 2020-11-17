# -*- coding: utf-8 -*-
# standard library
from datetime import datetime
from unittest.mock import Mock

__author__ = "Chaoyuuu (chaoyu2330@gmail.com)"
__license__ = "Apache 2.0"

# scip plugin
from spring_cloud.gateway.handler.predicate.core import AfterRoutePredicate, CookieRoutePredicate, PathRoutePredicate


class TestAfterRoutePredicate:
    def given_config_datetime(self, date_time: datetime):
        self.config = AfterRoutePredicate.Config(date_time)
        self.predicate = AfterRoutePredicate(self.config)

    def given_now(self, now: datetime):
        self.predicate.now_datetime_func = lambda: now

    def test_when_now_datatime_is_after_config_datetime_Then_return_T(self):
        self.given_config_datetime(datetime(2020, 11, 1))
        self.given_now(datetime(2020, 11, 11))
        value = self.predicate.test("whatever")
        assert value

    def test_When_now_datetime_is_not_after_config_datetime_Then_return_F(self):
        self.given_config_datetime(datetime(2020, 12, 1))
        self.given_now(datetime(2020, 11, 11))
        value = self.predicate.test("whatever")
        assert not value


class TestPathRoutePredicate:
    def given_config_pattern(self, pattern: str):
        self.config = PathRoutePredicate.Config(pattern)
        self.predicate = PathRoutePredicate(self.config)

    def given_request_url(self, request_url: str):
        self.http_request = Mock()
        self.http_request.path_patterns = request_url

    def test_Given_url_When_match_pattern_Then_return_T(self):
        self.given_config_pattern("/get")
        self.given_request_url("http://localhost:8080/get")
        value = self.predicate.test(self.http_request)
        assert value

    def test_Given_url_When_not_match_pattern_Then_return_F(self):
        self.given_config_pattern("/test")
        self.given_request_url("http://localhost:8080/get")
        value = self.predicate.test(self.http_request)
        assert not value


class TestCookieRoutePredicate:
    def given_config_cookie(self, cookie_name, cookie_value):
        self.config = CookieRoutePredicate.Config(cookie_name, cookie_value)
        self.predicate = CookieRoutePredicate(self.config)

    def give_http_cookies(self, http_cookies=None):
        self.http_request = Mock()
        self.http_request.cookies = http_cookies

    def test_Given_cookies_from_config_When_match_cookie_Then_return_T(self):
        self.given_config_cookie("my_cookie", "ch.p")
        self.give_http_cookies({"your_cookie": ["sugar"], "my_cookie": ["ch.p", "cookie"]})
        value = self.predicate.test(self.http_request)
        assert value

    def test_Given_cookies_from_config_When_not_match_cookie_Then_return_F(self):
        self.given_config_cookie("my_cookie", "ch.p")
        self.give_http_cookies({"your_cookie": ["sugar"], "his_cookie": ["chocolate", "truffle"]})
        value = self.predicate.test(self.http_request)
        assert not value

    def test_Given_no_cookies_from_config_When_test_Should_be_F(self):
        self.given_config_cookie("my_cookie", "ch.p")
        self.give_http_cookies()
        value = self.predicate.test(self.http_request)
        assert not value
