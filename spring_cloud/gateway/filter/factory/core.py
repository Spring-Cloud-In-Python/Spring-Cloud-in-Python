# -*- coding: utf-8 -*-
from __future__ import annotations

__author__ = "Chaoyuuu (chaoyu2330@gmail.com)"
__license__ = "Apache 2.0"

# scip plugin
from spring_cloud.gateway.filter import GatewayFilter, GatewayFilterChain
from spring_cloud.gateway.filter.factory.base import GatewayFilterFactory
from spring_cloud.gateway.server import GATEWAY_ALREADY_PREFIXED_ATTR, GATEWAY_REQUEST_URL_ATTR, ServerWebExchange
from spring_cloud.utils.logging import getLogger


class AddRequestHeaderGatewayFilterFactory(GatewayFilterFactory):
    def apply(self, config) -> GatewayFilter:
        return AddRequestHeaderGatewayFilter(config)


class AddResponseHeaderGatewayFilterFactory(GatewayFilterFactory):
    def apply(self, config) -> GatewayFilter:
        return AddResponseHeaderGatewayFilter(config)


class PrefixPathGatewayFilterFactory(GatewayFilterFactory):
    def apply(self, config) -> GatewayFilter:
        return PrefixPathGatewayFilter(config)


class AddRequestHeaderGatewayFilter(GatewayFilter):
    def __init__(self, config: NameValueConfig):
        self.config = config
        self.logger = getLogger(name="spring_cloud.gateway.filter.core")

    def filter(self, exchange: ServerWebExchange, chain: GatewayFilterChain) -> None:
        request = exchange.request.mutate().header(self.config.name, self.config.value).build()
        self.logger.trace(f"Add request header with: {self.config.name}={self.config.value}")
        chain.filter(exchange.mutate().request(request).build())


class AddResponseHeaderGatewayFilter(GatewayFilter):
    def __init__(self, config: NameValueConfig):
        self.config = config
        self.logger = getLogger(name="spring_cloud.gateway.filter.core")

    def filter(self, exchange: ServerWebExchange, chain: GatewayFilterChain) -> None:
        exchange.response.add_header(self.config.name, self.config.value)
        self.logger.trace(f"Add response header with: {self.config.name}={self.config.value}")
        chain.filter(exchange)


class PrefixPathGatewayFilter(GatewayFilter):
    def __init__(self, config: PrefixPathGatewayFilter.Config):
        self.config = config
        self.logger = getLogger(name="spring_cloud.gateway.filter.core")

    def filter(self, exchange: ServerWebExchange, chain: GatewayFilterChain) -> None:
        is_already_prefix = exchange.get_arrtibute_or_default(GATEWAY_ALREADY_PREFIXED_ATTR, False)
        if is_already_prefix:
            return chain.filter(exchange)

        exchange.attributes[GATEWAY_ALREADY_PREFIXED_ATTR] = True
        new_path = f"{self.config.prefix}{exchange.request.path}"
        request = exchange.request.mutate().path(new_path).build()
        exchange.attributes[GATEWAY_REQUEST_URL_ATTR] = f"{request.uri}{request.path}"
        self.logger.trace(f"Prefixed URI with: {self.config.prefix} -> {request.uri}{request.path}")
        chain.filter(exchange.mutate().request(request).build())

    class Config:
        def __init__(self, prefix: str):
            self.prefix = prefix


class NameValueConfig:
    def __init__(self, name: str, value: str):
        self.__name = name
        self.__value = value

    @property
    def name(self):
        return self.__name

    @property
    def value(self):
        return self.__value
