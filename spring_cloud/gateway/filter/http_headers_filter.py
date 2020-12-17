# -*- coding: utf-8 -*-
from __future__ import annotations

# standard library
import re
from abc import ABC, abstractmethod

__author__ = "Chaoyuuu (chaoyu2330@gmail.com)"
__license__ = "Apache 2.0"

# standard library
from enum import Enum
from typing import Dict, List

# scip plugin
from spring_cloud.gateway.server import ServerWebExchange
from spring_cloud.gateway.server.utils import GATEWAY_ORIGINAL_REQUEST_URL_ATTR, GATEWAY_REQUEST_URL_ATTR


class HttpHeadersFilter(ABC):
    @staticmethod
    def filter_request(filters: List[HttpHeadersFilter], exchange: ServerWebExchange) -> Dict[str, str]:
        return HttpHeadersFilter.filter_(filters, exchange.request.headers, exchange, Type.REQUEST)

    @staticmethod
    def filter_(
        filters: List[HttpHeadersFilter], headers: Dict[str, str], exchange: ServerWebExchange, type: Type
    ) -> Dict[str, str]:

        response_headers = headers
        for header_filter in filters:
            if header_filter.supports(type):
                response_headers = header_filter.filter(response_headers, exchange)

        return response_headers

    def supports(self, type: Type):
        return type == Type.REQUEST

    @abstractmethod
    def filter(self, original: Dict[str, str], exchange: ServerWebExchange) -> Dict[str, str]:
        raise NotImplemented


class Type(Enum):
    REQUEST = ("request",)
    RESPONSE = "response"


class ForwardedHeadersFilter(HttpHeadersFilter):
    FORWARDED_HEADER = "Forwarded"

    def filter(self, original: Dict[str, str], exchange: ServerWebExchange) -> Dict[str, str]:
        forwardeds = []
        updated = {key: val for key, val in original.items() if key.lower() != self.FORWARDED_HEADER.lower()}

        if original.get(self.FORWARDED_HEADER):
            forwardeds.append(original.get(self.FORWARDED_HEADER))

        forwardeds.append(f'host="{exchange.request.host}"')
        # TODO: the scheme should also be a variable
        forwardeds.append(f"proto=http")

        if exchange.request.remote_addr:
            forwardeds.append(f'for="{exchange.request.remote_addr[0]}:{exchange.request.remote_addr[1]}"')

        updated[self.FORWARDED_HEADER] = self.to_header_value(forwardeds)
        return updated

    def to_header_value(self, forwardeds: List[str]):
        return ";".join(forwardeds)


class XForwardedHeadersFilter(HttpHeadersFilter):
    X_FORWARDED_FOR_HEADER = "X-Forwarded-For"
    X_FORWARDED_PROTO_HEADER = "X-Forwarded-Proto"
    X_FORWARDED_PORT_HEADER = "X-Forwarded-Port"
    X_FORWARDED_HOST_HEADER = "X-Forwarded-Host"

    def __init__(self):
        self.__for_append = True
        self.__for_enabled = True
        self.__proto_enabled = True
        self.__proto_append = True
        self.__prefix_enabled = True
        self.__port_enabled = True
        self.__port_append = True
        self.__host_append = True
        self.__host_enabled = True

    @property
    def for_append(self):
        return self.__for_append

    @for_append.setter
    def for_append(self, for_append: bool):
        self.__for_append = for_append

    @property
    def for_enabled(self):
        return self.__for_enabled

    @for_enabled.setter
    def for_enabled(self, for_enabled: bool):
        self.__for_enabled = for_enabled

    @property
    def proto_enabled(self):
        return self.__proto_enabled

    @proto_enabled.setter
    def proto_enabled(self, proto_enabled: bool):
        self.__proto_enabled = proto_enabled

    @property
    def proto_append(self):
        return self.__proto_append

    @proto_append.setter
    def proto_append(self, proto_append: bool):
        self.__proto_append = proto_append

    @property
    def prefix_enabled(self):
        return self.__proto_enabled

    @prefix_enabled.setter
    def prefix_enabled(self, prefix_enabled: bool):
        self.__prefix_enabled = prefix_enabled

    @property
    def port_enabled(self):
        return self.__port_enabled

    @port_enabled.setter
    def port_enabled(self, port_enabled: bool):
        self.__port_enabled = port_enabled

    @property
    def port_append(self):
        return self.__port_append

    @port_append.setter
    def port_append(self, port_append: bool):
        self.__port_append = port_append

    @property
    def host_enabled(self):
        return self.__host_enabled

    @host_enabled.setter
    def host_enabled(self, host_enabled: bool):
        self.__host_enabled = host_enabled

    @property
    def host_append(self):
        return self.__host_append

    @host_append.setter
    def host_append(self, host_append: bool):
        self.__host_append = host_append

    def filter(self, original: Dict[str, str], exchange: ServerWebExchange) -> Dict[str, str]:
        updated = original.copy()
        request = exchange.request

        if self.for_enabled and request.remote_addr:
            local_addr = request.local_addr
            self.write(updated, self.X_FORWARDED_FOR_HEADER, local_addr[0], self.for_append)

        if self.proto_enabled:
            self.write(updated, self.X_FORWARDED_PROTO_HEADER, "http", self.proto_append)

        # TODO: Implement X-Forwarded-Prefix header
        if self.prefix_enabled:
            original_uris = exchange.attributes.get(GATEWAY_ORIGINAL_REQUEST_URL_ATTR)
            request_uri = exchange.attributes.get(GATEWAY_REQUEST_URL_ATTR)
            if original_uris and request_uri:
                pass

        if self.port_enabled:
            self.write(updated, self.X_FORWARDED_PORT_HEADER, str(request.port), self.port_append)

        if self.host_enabled:
            self.write(updated, self.X_FORWARDED_HOST_HEADER, f"{request.host}:{request.port}", self.host_append)

        return updated

    def write(self, headers: Dict[str, str], key: str, value: str, append: bool):
        if append and headers.get(key):
            values = headers[key]
            headers[key] = f"{values},{value}"
        else:
            headers[key] = value


class RemoveHopByHopHeadersFilter(HttpHeadersFilter):
    HEADERS_REMOVED_ON_REQUEST = {
        "connection",
        "keep-alive",
        "transfer-encoding",
        "te",
        "trailer",
        "proxy-authorization",
        "proxy-authenticate",
        "x-application-context",
        "upgrade",
    }

    def filter(self, original: Dict[str, str], exchange: ServerWebExchange) -> Dict[str, str]:
        updated = {}
        for key, value in original.items():
            if not any(key.lower() == header.lower() for header in self.HEADERS_REMOVED_ON_REQUEST):
                updated[key] = value

        return updated


HEADER_FILTERS = [ForwardedHeadersFilter(), XForwardedHeadersFilter(), RemoveHopByHopHeadersFilter()]
