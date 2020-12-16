# -*- coding: utf-8 -*-
# standard library
from abc import ABC, abstractmethod
from typing import Dict

# pypi/conda library
import requests

__author__ = "Chaoyuuu (chaoyu2330@gmail.com)"
__license__ = "Apache 2.0"

# scip plugin
from spring_cloud.commons.http import RestTemplate
from spring_cloud.gateway.filter import (
    ForwardedHeadersFilter,
    GatewayFilterChain,
    HttpHeadersFilter,
    RemoveHopByHopHeadersFilter,
    XForwardedHeadersFilter,
)
from spring_cloud.gateway.server import ServerWebExchange
from spring_cloud.gateway.server.utils import is_already_routed, set_already_routed


class GlobalFilter(ABC):
    @abstractmethod
    def filter(self, exchange: ServerWebExchange, chain: GatewayFilterChain):
        return NotImplemented


class RestTemplateRouteFilter(GlobalFilter):
    def __init__(self, rest_template: RestTemplate):
        self.api = rest_template
        self.header_filters = [ForwardedHeadersFilter(), XForwardedHeadersFilter(), RemoveHopByHopHeadersFilter()]

    def filter(self, exchange: ServerWebExchange, chain: GatewayFilterChain):
        if is_already_routed(exchange):
            return chain.filter(exchange)
        set_already_routed(exchange)

        method = exchange.request.method
        url = self.compose_url(exchange.request.uri, exchange.request.path)
        filtered_headers = HttpHeadersFilter.filter_request(self.header_filters, exchange)
        headers = self.compose_headers(exchange.request.cookies, filtered_headers)
        headers_removed = self.remove_host_header(headers)
        params = exchange.request.query

        res = self.map_api_request_method(method)(url, headers=headers_removed, params=params)
        self.send(res, exchange)

    def map_api_request_method(self, method: str):
        method = method.lower()
        mapping = {
            "get": self.api.get,
            "put": self.api.put,
            "post": self.api.post,
            "patch": self.api.patch,
            "options": self.api.options,
            "delete": self.api.delete,
            "head": self.api.head,
        }
        return mapping[method]

    def send(self, res: requests.Response, exchange: ServerWebExchange):
        self.set_content_header(res.headers, res.content)
        exchange.response.set_body(res.content)
        exchange.response.set_status_code(res.status_code)
        exchange.response.set_headers(**res.headers)
        exchange.response.commit()

    @classmethod
    def compose_url(cls, uri: str, path: str):
        return uri + path

    @classmethod
    def compose_headers(cls, cookies: Dict[str, str], filtered_headers: Dict[str, str]):
        return {**cookies, **filtered_headers}

    def remove_host_header(self, headers: Dict[str, str]):
        headers.pop("Host", None)
        headers.pop("X-Forwarded-For", None)

    def set_content_header(self, headers: Dict[str, str], body: bytes):
        headers.pop("Content-Encoding", None)
        headers["Content-Length"] = str(len(body))
