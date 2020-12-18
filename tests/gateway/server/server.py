# -*- coding: utf-8 -*-
__author__ = "Chaoyuuu (chaoyu2330@gmail.com)"
__license__ = "Apache 2.0"

# standard library
from typing import Dict

# scip plugin
from spring_cloud.gateway.server import ServerHTTPRequest, ServerHTTPResponse, ServerWebExchange
from spring_cloud.utils.validate import not_none


class StubServerWebExchange(ServerWebExchange):
    def __init__(self, http_request: ServerHTTPRequest, http_response: ServerHTTPResponse):
        self.__request = http_request
        self.__response = http_response
        self.__attributes = {}

    @property
    def request(self) -> ServerHTTPRequest:
        return self.__request

    @property
    def response(self) -> ServerHTTPResponse:
        return self.__response

    @request.setter
    def request(self, request: ServerHTTPRequest):
        self.__request = request

    @response.setter
    def response(self, response: ServerHTTPResponse):
        self.__response = response

    @property
    def attributes(self) -> Dict[str, object]:
        return self.__attributes

    def mutate(self) -> ServerWebExchange.Builder:
        return StubServerWebExchangeBuilder(self)


class StubServerWebExchangeBuilder(ServerWebExchange.Builder):
    def __init__(self, delegate: ServerWebExchange):
        not_none(delegate)
        self.__delegate = delegate
        self.__request = None
        self.__response = None

    def request(self, request: ServerHTTPRequest) -> ServerWebExchange.Builder:
        self.__delegate.request = request
        return self

    def response(self, response: ServerHTTPResponse) -> ServerWebExchange.Builder:
        self.__delegate.response = response
        return self

    def build(self) -> ServerWebExchange:
        return self.__delegate
