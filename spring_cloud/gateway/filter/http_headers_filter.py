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
        filters: List[HttpHeadersFilter], input_: Dict[str, str], exchange: ServerWebExchange, type: Type
    ) -> Dict[str, str]:

        response = input_
        for header_filter in filters:
            if header_filter.supports(type):
                response = header_filter.filter(response, exchange)

        return response

    def supports(self, type: Type):
        return type == Type.REQUEST

    @abstractmethod
    def filter(self, original: Dict[str, str], exchange: ServerWebExchange) -> Dict[str, str]:
        return NotImplemented


class Type(Enum):
    REQUEST = ("request",)
    RESPONSE = "response"


class ForwardedHeadersFilter(HttpHeadersFilter):
    FORWARDED_HEADER = "Forwarded"

    def filter(self, original: Dict[str, str], exchange: ServerWebExchange) -> Dict[str, str]:
        updated = {}
        forwardeds = []

        for key, value in original.items():
            if not re.match(key.lower(), self.FORWARDED_HEADER.lower()):
                updated[key] = value

        if original.get(self.FORWARDED_HEADER):
            forwardeds.append(original.get(self.FORWARDED_HEADER))

        forwardeds.append(f'host="{exchange.request.host}"')
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
    for_append = True
    for_enabled = True
    proto_enabled = True
    proto_append = True
    prefix_enabled = True
    port_enabled = True
    port_append = True
    host_append = True
    host_enabled = True

    def is_for_append(self):
        return self.for_append

    def set_for_append(self, for_append: bool):
        self.for_append = for_append

    def is_for_enabled(self):
        return self.for_enabled

    def set_for_enabled(self, for_enabled: bool):
        self.for_enabled = for_enabled

    def is_proto_enabled(self):
        return self.proto_enabled

    def set_proto_enabled(self, proto_enabled: bool):
        self.proto_enabled = proto_enabled

    def is_proto_append(self):
        return self.proto_append

    def set_proto_append(self, proto_append: bool):
        self.proto_append = proto_append

    def is_prefix_enabled(self):
        return self.proto_enabled

    def set_prefix_enabled(self, prefix_enabled: bool):
        self.prefix_enabled = prefix_enabled

    def is_port_enabled(self):
        return self.port_enabled

    def set_port_enable(self, port_enable: bool):
        self.port_enabled = port_enable

    def is_port_append(self):
        return self.port_append

    def set_port_append(self, port_append: bool):
        self.port_append = port_append

    def is_host_enabled(self):
        return self.host_enabled

    def set_host_enable(self, host_enable: bool):
        self.host_enabled = host_enable

    def is_host_append(self):
        return self.host_append

    def set_host_append(self, host_append: bool):
        self.host_append = host_append

    def filter(self, original: Dict[str, str], exchange: ServerWebExchange) -> Dict[str, str]:
        updated = original.copy()
        request = exchange.request

        if self.is_for_enabled() and request.remote_addr:
            local_addr = request.local_addr
            self.write(updated, self.X_FORWARDED_FOR_HEADER, local_addr[0], self.is_for_append())

        if self.is_proto_enabled():
            self.write(updated, self.X_FORWARDED_PROTO_HEADER, "http", self.is_proto_append())

        # TODO
        if self.is_prefix_enabled():
            original_uris = exchange.attributes.get(GATEWAY_ORIGINAL_REQUEST_URL_ATTR)
            request_uri = exchange.attributes.get(GATEWAY_REQUEST_URL_ATTR)
            if original_uris and request_uri:
                pass

        if self.is_port_enabled():
            self.write(updated, self.X_FORWARDED_PORT_HEADER, str(request.port), self.is_port_append())

        if self.is_host_enabled():
            self.write(updated, self.X_FORWARDED_HOST_HEADER, f"{request.host}:{request.port}", self.is_host_append())

        return updated

    def write(self, headers: Dict[str, str], key: str, value: str, append: bool):
        if append and headers.get(key):
            values = headers[key]
            headers[key] = f"{values},{value}"
        else:
            headers[key] = value


class RemoveHopByHopHeadersFilter(HttpHeadersFilter):
    HEADERS_REMOVED_ON_REQUEST = [
        "connection",
        "keep-alive",
        "transfer-encoding",
        "te",
        "trailer",
        "proxy-authorization",
        "proxy-authenticate",
        "x-application-context",
        "upgrade",
    ]

    def filter(self, original: Dict[str, str], exchange: ServerWebExchange) -> Dict[str, str]:
        updated = {}
        for key, value in original.items():
            if not any(re.match(key.lower(), header.lower()) for header in self.HEADERS_REMOVED_ON_REQUEST):
                updated[key] = value

        return updated
