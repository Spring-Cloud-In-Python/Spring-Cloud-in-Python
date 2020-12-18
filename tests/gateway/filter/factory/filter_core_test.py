# -*- coding: utf-8 -*-
# standard library
from unittest.mock import Mock

__author__ = "Chaoyuuu (chaoyu2330@gmail.com)"
__license__ = "Apache 2.0"

# scip plugin
from spring_cloud.gateway.filter.factory.core import (
    AddRequestHeaderGatewayFilter,
    AddResponseHeaderGatewayFilter,
    NameValueConfig,
    PrefixPathGatewayFilter,
)
from spring_cloud.gateway.server import ServerHTTPResponse, StaticServerHttpRequest
from tests.gateway.server.server import StubServerWebExchange


class TestAddRequestHeaderGatewayFilter:
    def given_exchange(self):
        http_response = Mock()
        http_request = StaticServerHttpRequest()
        self.exchange = StubServerWebExchange(http_request, http_response)

    def given_gateway_filter_config(self, header_name: str, header_value: str):
        self.config = NameValueConfig(header_name, header_value)
        self.filter_chain = Mock()
        self.gateway_filter = AddRequestHeaderGatewayFilter(self.config)

    def test_When_filter_Then_add_request_header(self):
        self.given_exchange()
        self.given_gateway_filter_config("Hello", "World")
        self.gateway_filter.filter(self.exchange, self.filter_chain)
        assert self.exchange.request.headers["Hello"] == "World"
        self.filter_chain.filter.assert_called_with(self.exchange)


class TestAddResponseHeaderGatewayFilter:
    def given_exchange(self):
        request_handler = Mock()
        http_response = ServerHTTPResponse(request_handler)
        http_request = StaticServerHttpRequest()
        self.exchange = StubServerWebExchange(http_request, http_response)

    def given_gateway_filter_config(self, header_name: str, header_value: str):
        self.config = NameValueConfig(header_name, header_value)
        self.filter_chain = Mock()
        self.gateway_filter = AddResponseHeaderGatewayFilter(self.config)

    def test_When_filter_Then_add_request_header(self):
        self.given_exchange()
        self.given_gateway_filter_config("Hello", "World")
        self.gateway_filter.filter(self.exchange, self.filter_chain)
        assert self.exchange.response.headers["Hello"] == "World"
        self.filter_chain.filter.assert_called_with(self.exchange)


class TestPrefixPathGatewayFilter:
    def given_exchange(self, url: str):
        http_response = Mock()
        http_request = StaticServerHttpRequest(url_=url)
        self.exchange = StubServerWebExchange(http_request, http_response)

    def given_gateway_filter_config(self, prefix: str):
        self.config = PrefixPathGatewayFilter.Config(prefix)
        self.filter_chain = Mock()
        self.gateway_filter = PrefixPathGatewayFilter(self.config)

    def test_When_filter_Then_add_request_header(self):
        self.given_exchange("http://127.0.0.1:8888/get")
        self.given_gateway_filter_config("/prefix")
        self.gateway_filter.filter(self.exchange, self.filter_chain)
        assert self.exchange.request.path == "/prefix/get"
        self.filter_chain.filter.assert_called_with(self.exchange)
