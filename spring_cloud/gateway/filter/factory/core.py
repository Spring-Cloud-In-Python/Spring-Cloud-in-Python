# -*- coding: utf-8 -*-

__author__ = "Chaoyuuu (chaoyu2330@gmail.com)"
__license__ = "Apache 2.0"

# scip plugin
from spring_cloud.gateway.filter.factory.base import GatewayFilterFactory
from spring_cloud.gateway.filter.factory.filter import GatewayFilter


class AddResponseHeaderGatewayFilterFactory(GatewayFilterFactory):
    def apply(self, config) -> GatewayFilter:
        return AddRequestHeaderGatewayFilter(config)


class ModifyRequestBodyGatewayFilterFactory(GatewayFilterFactory):
    def apply(self, config) -> GatewayFilter:
        return AddResponseHeaderGatewayFilter(config)


class AddRequestHeaderGatewayFilter(GatewayFilter):
    def __init__(self, config):
        self.config = config

    # TODO: the header is dependency with http_request, but we haven't decided the tool,
    #  that is, the type of the cookies may be change in future
    def filter(self, http_request, chain=None):
        http_request.header[self.config.header_name] = self.config.header_value
        chain.filter(http_request)
        # exchange.request.header.add(self.config.name, self.config.value)
        # return chain.filter(http_request)


class AddResponseHeaderGatewayFilter(GatewayFilter):
    def __init__(self, config):
        self.config = config

    def filter(self, http_response, chain=None):
        http_response.header[self.config.header_name] = self.config.header_value
        chain.filter(http_response)


class ServerWebExchange:
    def __init__(self):
        self.response = None
        self.request = None


class GatewayFilterChain:
    def filter(self, exchange):
        # return Mono<void>
        pass
