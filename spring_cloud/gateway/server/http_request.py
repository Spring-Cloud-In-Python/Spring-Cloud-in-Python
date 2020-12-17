# -*- coding: utf-8 -*-
from __future__ import annotations

# standard library
import re
from abc import ABC, abstractmethod
from email.message import Message
from socket import socket
from socketserver import BaseServer
from typing import Dict, Optional
from urllib.parse import urlparse

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

    @property
    @abstractmethod
    def remote_addr(self) -> Optional[tuple]:
        raise NotImplemented

    @property
    @abstractmethod
    def local_addr(self) -> Optional[tuple]:
        raise NotImplemented

    @property
    @abstractmethod
    def host(self) -> str:
        raise NotImplemented

    @property
    @abstractmethod
    def port(self) -> int:
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
    def __init__(self, headers: Message, path: str, server: BaseServer, method: str, rfile: BinaryIO, request: socket):
        self.__headers = headers
        self.__path = path
        self.__server = server
        self.__rfile = rfile
        self.__method = method
        self.__request = request

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

    @property
    def remote_addr(self) -> Optional[tuple]:
        return self.__request.getpeername()

    @property
    def local_addr(self) -> Optional[tuple]:
        return self.__request.getsockname()


class DefaultServerHttpRequestBuilder(ServerHTTPRequest.Builder):
    def __init__(self, original: ServerHTTPRequest):
        not_none(original)
        self.__method = original.method
        self.__uri = original.uri
        self.__path = original.path
        self.__headers = original.headers
        self.__original_request = original

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
        return MutatedServerHttpRequest(self.__uri, self.__headers, self.__method, self.__original_request, self.__path)


class MutatedServerHttpRequest(ServerHTTPRequest):
    def __init__(
        self, uri: str, headers: Dict[str, str], method: str, request: ServerHTTPRequest, path: str,
    ):
        self.__uri = uri
        self.__headers = headers
        self.__method = method
        self.__original_request = request
        self.__path = path

    @property
    def path(self) -> str:
        return self.__path

    @property
    def query(self) -> Dict[str, str]:
        return self.__original_request.query

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
        return self.__original_request.body

    @property
    def remote_addr(self) -> Optional[tuple]:
        return self.__original_request.remote_addr

    @property
    def local_addr(self) -> Optional[tuple]:
        return self.__original_request.local_addr

    @property
    def host(self) -> str:
        return self.__original_request.host

    @property
    def port(self) -> int:
        return self.__original_request.port


class StaticServerHttpRequest(ServerHTTPRequest):
    def __init__(
        self,
        headers: Dict[str, str] = {},
        url_: str = "http://127.0.0.1:8888/get",
        method: str = "GET",
        cookies: Dict[str, str] = {},
        body: bytearray = b"",
        query: Dict[str, str] = {},
        remote_addr: Optional[tuple] = ("10.0.0.1", 51630),
        local_addr: Optional[tuple] = ("10.0.0.1", 51333),
    ):
        urlparse_ = urlparse(url_)
        self.__headers = headers
        self.__method = method
        self.__cookies = cookies
        self.__url = url_
        self.__path = urlparse_.path
        self.__host = urlparse_.hostname
        self.__port = urlparse_.port
        self.__body = body
        self.__query = query
        self.__remote_addr = remote_addr
        self.__local_addr = local_addr

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
        return self.__url

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

    @property
    def remote_addr(self) -> Optional[tuple]:
        return self.__remote_addr

    @property
    def local_addr(self) -> Optional[tuple]:
        return self.__local_addr
