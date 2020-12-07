# -*- coding: utf-8 -*-
from __future__ import annotations

# standard library
from http.server import HTTPServer, SimpleHTTPRequestHandler

__author__ = "Chaoyuuu (chaoyu2330@gmail.com)"
__license__ = "Apache 2.0"

# standard library
from abc import ABC, abstractmethod
from typing import Dict

# scip plugin
from spring_cloud.gateway.server.http_request import DefaultServerHttpRequest, ServerHTTPRequest
from spring_cloud.utils.validate import not_none


class ServerHTTPResponse:
    def __init__(self, handler: HTTPRequestHandler):
        self.__status_code = 200
        self.__cookies = {}
        self.__headers = {}
        self.__body = ""
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

    def set_body(self, body: str):
        self.__body = body

    def commit(self):
        self.__handler.send_response(self.__status_code)
        self.add_cookie_headers()
        for key in self.__headers.keys():
            self.__handler.send_header(key, self.__headers.get(key))
        self.__handler.end_headers()
        self.__handler.wfile.write(bytes(self.__body, "utf-8"))

    def add_cookie_headers(self):
        cookies = [f"{key} = {self.__cookies.get(key)}" for key in self.__cookies.keys()]
        header_value = ""
        if len(cookies) != 0:
            for cookie in cookies:
                if len(cookies) == 1:
                    header_value = f"{cookie}"
                else:
                    header_value = f"{cookie}; {header_value}"
            self.__headers["Cookie"] = header_value


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
    def attribute(self) -> Dict[str, object]:
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
        return self.__request if self.__request else self.__delegate.request

    @property
    def response(self) -> ServerHTTPResponse:
        return self.__response if self.__response else self.__delegate.response

    @property
    def attribute(self) -> Dict[str, object]:
        return self.__delegate.attribute


class DefaultServerWebExchange(ServerWebExchange):
    def __init__(self, http_request: ServerHTTPRequest, http_response: ServerHTTPResponse):
        self.__request = http_request
        self.__response = http_response
        self.__attributes = {}

    @property
    def request(self) -> ServerHTTPRequest:
        return self.__request

    @property
    def request_header(self) -> Dict[str, str]:
        return self.__request.headers

    @property
    def response(self) -> ServerHTTPResponse:
        return self.__response

    @property
    def response_header(self) -> Dict[str, str]:
        return self.__response.headers

    @property
    def attribute(self) -> Dict[str, object]:
        return self.__attributes

    def get_required_attribute(self, name: str) -> object:
        return not_none(self.__attributes[name])

    # TODO: will be implement if we need this in future
    @property
    def checkNotModified(self) -> bool:
        pass


class HTTPRequestHandler(SimpleHTTPRequestHandler):
    def handle_(self):
        http_request = DefaultServerHttpRequest(self.headers, self.path, self.server, self.command, self.rfile)
        http_response = ServerHTTPResponse(self)
        exchange = DefaultServerWebExchange(http_request, http_response)
        # scip plugin
        from spring_cloud.gateway.handler.handler import DispatcherHandler

        DispatcherHandler().handle(exchange)

    def do_GET(self):
        self.handle_()

    def do_POST(self):
        self.handle_()

    def do_PUT(self):
        self.handle_()

    def do_PATCH(self):
        self.handle_()

    def do_DELETE(self):
        self.handle_()

    def de_COPY(self):
        self.handle_()

    def do_HEAD(self):
        self.handle_()

    def do_OPTIONS(self):
        self.handle_()

    def de_LINK(self):
        self.handle_()

    def de_UNLINK(self):
        self.handle_()

    def de_LOCK(self):
        self.handle_()

    def de_UNLOCK(self):
        self.handle_()

    def de_PROPFIND(self):
        self.handle_()

    def de_VIEW(self):
        self.handle_()


if __name__ == "__main__":

    hostName = "localhost"
    serverPort = 8888

    webServer = HTTPServer((hostName, serverPort), HTTPRequestHandler)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")
