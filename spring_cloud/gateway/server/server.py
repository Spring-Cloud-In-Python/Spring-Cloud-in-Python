# -*- coding: utf-8 -*-
from __future__ import annotations

# standard library
from abc import ABC, abstractmethod
from typing import Dict

__author__ = "Chaoyuuu (chaoyu2330@gmail.com)"
__license__ = "Apache 2.0"

# scip plugin
from spring_cloud.gateway.server.http_request import ServerHTTPRequest
from spring_cloud.utils.validate import not_none


class HttpResponseHandler(ABC):
    @abstractmethod
    def send_response(self, status_code: int):
        raise NotImplemented

    @abstractmethod
    def send_header(self, key: str, value: str):
        raise NotImplemented

    @abstractmethod
    def end_headers(self):
        raise NotImplemented

    @abstractmethod
    def write_body(self, body: bytearray):
        raise NotImplemented

    @abstractmethod
    def flush_headers(self):
        raise NotImplemented


class ServerHTTPResponse:
    def __init__(self, handler: HttpResponseHandler):
        self.__status_code = None
        self.__cookies = {}
        self.__headers = {}
        self.__body = bytearray()
        self.__handler = handler

    @property
    def status_code(self) -> int:
        return self.__status_code

    def set_status_code(self, status_code: int):
        self.__status_code = status_code

    @property
    def cookies(self) -> Dict[str, str]:
        return self.__cookies

    def add_cookie(self, key: str, value: str):
        self.__cookies[key] = value

    @property
    def headers(self) -> Dict[str, str]:
        return self.__headers

    def add_header(self, key: str, value: str):
        self.__headers[key] = value

    @property
    def body(self):
        return self.__body

    def set_body(self, body: bytearray):
        self.__body.extend(body)

    def commit(self):
        not_none(self.__status_code)
        self.__handler.send_response(self.__status_code)
        self.add_cookie_header()
        for key, value in self.__headers.items():
            self.__handler.send_header(key, value)
        self.__handler.end_headers()
        self.__handler.write_body(self.__body)

    def add_cookie_header(self):
        cookies = [f"{key}={value}" for key, value in self.__cookies.items()]
        self.__headers["Cookie"] = ";".join(cookies)


class ServerWebExchange(ABC):
    @property
    @abstractmethod
    def request(self) -> ServerHTTPRequest:
        raise NotImplemented

    @property
    @abstractmethod
    def response(self) -> ServerHTTPResponse:
        raise NotImplemented

    @property
    @abstractmethod
    def attributes(self) -> Dict[str, object]:
        raise NotImplemented

    def mutate(self) -> ServerWebExchange.Builder:
        return DefaultServerWebExchangeBuilder(self)

    class Builder(ABC):
        @abstractmethod
        def request(self, request: ServerHTTPRequest) -> ServerWebExchange.Builder:
            raise NotImplemented

        @abstractmethod
        def response(self, response: ServerHTTPResponse) -> ServerWebExchange.Builder:
            raise NotImplemented

        @abstractmethod
        def build(self) -> ServerWebExchange:
            raise NotImplemented


class DefaultServerWebExchangeBuilder(ServerWebExchange.Builder):
    def __init__(self, delegate: ServerWebExchange):
        not_none(delegate)
        self.__delegate = delegate
        self.__request = None
        self.__response = None

    def request(self, request: ServerHTTPRequest) -> ServerWebExchange.Builder:
        self.__request = request
        return self

    def response(self, response: ServerHTTPResponse) -> ServerWebExchange.Builder:
        self.__response = response
        return self

    def build(self) -> ServerWebExchange:
        return MutativeServerWebExchange(self.__delegate, self.__request, self.__response)


class MutativeServerWebExchange(ServerWebExchange):
    def __init__(self, delegate: ServerWebExchange, request: ServerHTTPRequest, response: ServerHTTPResponse):
        self.__delegate = delegate
        self.__request = request
        self.__response = response

    @property
    def request(self) -> ServerHTTPRequest:
        return self.__request or self.__delegate.request

    @property
    def response(self) -> ServerHTTPResponse:
        return self.__response or self.__delegate.response

    @property
    def attributes(self) -> Dict[str, object]:
        return self.__delegate.attributes


class DefaultServerWebExchange(ServerWebExchange):
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

    @property
    def attributes(self) -> Dict[str, object]:
        return self.__attributes

    def get_required_attribute(self, name: str) -> object:
        return not_none(self.__attributes[name])

    # TODO: will be implement if we need this in future
    @property
    def checkNotModified(self) -> bool:
        raise NotImplemented
