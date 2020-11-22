# -*- coding: utf-8 -*-
# standard library
from unittest.mock import Mock

__author__ = "Chaoyuuu (chaoyu2330@gmail.com)"
__license__ = "Apache 2.0"

# scip plugin
from spring_cloud.gateway.filter import StaticGatewayFilterChain
from spring_cloud.gateway.filter.factory import AddRequestHeaderGatewayFilter, AddResponseHeaderGatewayFilter


class TestAddRequestHeaderGatewayFilter:
    def given_http_request_header(self, header):
        self.http_request = Mock()
        self.http_request.header = header

    def given_gateway_filter_config(self, header_name, header_value):
        self.config = Mock()
        self.config.header_name = header_name
        self.config.header_value = header_value
        self.gateway_filter = AddRequestHeaderGatewayFilter(self.config)
        self.filter_chain = StaticGatewayFilterChain()

    def test_When_filter_Then_add_request_header(self):
        self.given_http_request_header({})
        self.given_gateway_filter_config("Hello", "World")
        self.gateway_filter.filter(self.http_request, self.filter_chain)
        assert self.http_request.header["Hello"] == "World"


class TestAddResponseHeaderGatewayFilter:
    def given_http_response_header(self, header):
        self.http_response = Mock()
        self.http_response.header = header

    def given_gateway_filter_config(self, header_name, header_value):
        self.config = Mock()
        self.config.header_name = header_name
        self.config.header_value = header_value
        self.filter_chain = StaticGatewayFilterChain()
        self.gateway_filter = AddResponseHeaderGatewayFilter(self.config)

    def test_When_filter_Then_add_request_header(self):
        self.given_http_response_header({})
        self.given_gateway_filter_config("Hello", "World")
        self.gateway_filter.filter(self.http_response, self.filter_chain)
        assert self.http_response.header["Hello"] == "World"
