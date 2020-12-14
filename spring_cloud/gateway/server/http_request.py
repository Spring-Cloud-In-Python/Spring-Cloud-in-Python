# -*- coding: utf-8 -*-
from __future__ import annotations

# standard library
import re
from abc import ABC, abstractmethod
from email.message import Message
from socketserver import BaseServer
from typing import Dict

__author__ = "Chaoyuuu (chaoyu2330@gmail.com)"
__license__ = "Apache 2.0"

# standard library
from typing.io import BinaryIO

# scip plugin
from spring_cloud.utils.validate import not_none


class ServerHTTPRequest(ABC):
    @property
    @abstractmethod
    def path(self) -> str:
        raise NotImplemented

    @property
    @abstractmethod
    def query(self) -> Dict[str, str]:
        raise NotImplemented

    @property
    @abstractmethod
    def cookies(self) -> Dict[str, str]:
        raise NotImplemented

    @property
    @abstractmethod
    def method(self) -> str:
        raise NotImplemented

    @property
    @abstractmethod
    def uri(self) -> str:
        raise NotImplemented

    @property
    @abstractmethod
    def headers(self) -> Dict[str, str]:
        raise NotImplemented

    @property
    @abstractmethod
    def body(self) -> bytes:
        raise NotImplemented

    def mutate(self) -> ServerHTTPRequest.Builder:
        return DefaultServerHttpRequestBuilder(self)

    class Builder(ABC):
        @abstractmethod
        def method(self, method: str) -> ServerHTTPRequest.Builder:
            raise NotImplemented

        @abstractmethod
        def uri(self, uri: str) -> ServerHTTPRequest.Builder:
            raise NotImplemented

        @abstractmethod
        def path(self, path: str) -> ServerHTTPRequest.Builder:
            raise NotImplemented

        @abstractmethod
        def header(self, key: str, value: str) -> ServerHTTPRequest.Builder:
            raise NotImplemented

        @abstractmethod
        def build(self) -> ServerHTTPRequest:
            raise NotImplemented


class DefaultServerHttpRequest(ServerHTTPRequest):
    def __init__(self, headers: Message, path: str, server: BaseServer, method: str, rfile: BinaryIO):
        self.__headers = headers
        self.__path = path
        self.__server = server
        self.__rfile = rfile
        self.__method = method

    @property
    def path(self) -> str:
        return self.__path.split(r"?")[0]

    @property
    def query(self) -> Dict[str, str]:
        token = self.__path.split(r"?")
        query = {}
        if len(token) == 2:
            for segment in re.split(r"\s*&\s*", token[1]):
                key, value = re.split(r"\s*=\s*", segment)[:2]
                query[key] = value
        return query

    @property
    def cookies(self) -> Dict[str, str]:
        cookies = {}
        value = self.__headers.get("Cookie")
        if value:
            for segment in re.split(r"\s*;\s*", value):
                key, value = re.split(r"\s*=\s*", segment)[:2]
                cookies[key] = value
        return cookies

    @property
    def method(self) -> str:
        return self.__method

    # TODO: the current version doesn't support https
    @property
    def uri(self) -> str:
        return f"http://{self.host}:{self.port}"

    @property
    def headers(self) -> Dict[str, str]:
        return dict(self.__headers._headers)

    @property
    def body(self) -> bytes:
        if "Content-Length" in self.__headers.keys():
            content_len = int(self.__headers.get("Content-Length"))
            return self.__rfile.read(content_len)
        else:
            return b""

    @property
    def host(self) -> str:
        return self.__server.server_address[0]

    @property
    def port(self) -> int:
        return self.__server.server_address[1]


class DefaultServerHttpRequestBuilder(ServerHTTPRequest.Builder):
    def __init__(self, original: ServerHTTPRequest):
        not_none(original)
        self.__uri = original.uri
        self.__headers = original.headers
        self.__method = original.method
        self.__body = original.body
        self.__original_request = original
        self.__path = original.path
        self.__query = original.query

    def method(self, method_: str) -> ServerHTTPRequest.Builder:
        self.__method = method_
        return self

    def uri(self, uri: str) -> ServerHTTPRequest.Builder:
        self.__uri = uri
        return self

    def path(self, path: str) -> ServerHTTPRequest.Builder:
        self.__path = path
        return self

    def header(self, key: str, value: str) -> ServerHTTPRequest.Builder:
        self.__headers[key] = value
        return self

    def build(self) -> ServerHTTPRequest:
        return MutatedServerHttpRequest(
            self.__uri, self.__headers, self.__method, self.__body, self.__original_request, self.__path, self.__query
        )


class MutatedServerHttpRequest(ServerHTTPRequest):
    def __init__(
        self,
        uri: str,
        headers: Dict[str, str],
        method: str,
        body: bytes,
        request: ServerHTTPRequest,
        path: str,
        query: Dict[str, str],
    ):
        self.__method = method
        self.__body = body
        self.__original_request = request
        self.__uri = uri
        self.__path = path
        self.__headers = headers
        self.__query = query

    @property
    def path(self) -> str:
        return self.__path

    @property
    def query(self) -> Dict[str, str]:
        return self.__query

    @property
    def cookies(self) -> Dict[str, str]:
        return self.__original_request.cookies

    @property
    def method(self) -> str:
        return self.__method

    @property
    def uri(self) -> str:
        return self.__uri

    @property
    def headers(self) -> Dict[str, str]:
        return self.__headers

    @property
    def body(self) -> bytes:
        return self.__body


class StaticServerHttpRequest(ServerHTTPRequest):
    def __init__(
        self,
        headers: Dict[str, str] = {},
        path: str = "/get",
        method: str = "GET",
        cookies: Dict[str, str] = {},
        port: int = 8888,
        host: str = "127.0.0.1",
        body: bytearray = b"",
        query: Dict[str, str] = {},
    ):
        self.__headers = headers
        self.__path = path
        self.__method = method
        self.__cookies = cookies
        self.__port = port
        self.__host = host
        self.__body = body
        self.__query = query

    @property
    def path(self) -> str:
        return self.__path

    @property
    def query(self) -> Dict[str, str]:
        return self.__query

    @property
    def cookies(self) -> Dict[str, str]:
        return self.__cookies

    @property
    def method(self) -> str:
        return self.__method

    # TODO: the current version doesn't support https
    @property
    def uri(self) -> str:
        return f"http://{self.host}:{self.port}"

    @property
    def headers(self) -> Dict[str, str]:
        return self.__headers

    @property
    def body(self) -> bytes:
        return self.__body

    @property
    def host(self) -> str:
        return self.__host

    @property
    def port(self) -> int:
        return self.__port
