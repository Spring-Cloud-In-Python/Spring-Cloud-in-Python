# -*- coding: utf-8 -*-

__author__ = "Chaoyuuu (chaoyu2330@gmail.com)"
__license__ = "Apache 2.0"

# scip plugin
from spring_cloud.gateway.server import ServerWebExchange

GATEWAY_ROUTE_ATTR = "gatewayRoute"
GATEWAY_HANDLER_MAPPER_ATTR = "gatewayHandlerMapper"
GATEWAY_PREDICATE_ROUTE_ATTR = "gatewayPredicateRouteAttr"
GATEWAY_REQUEST_URL_ATTR = "gatewayRequestUrl"
GATEWAY_ALREADY_ROUTED_ATTR = "gatewayAlreadyRoutedAttr"
GATEWAY_ORIGINAL_REQUEST_URL_ATTR = "gatewayOriginalRequestUrl"


def is_already_routed(exchange: ServerWebExchange):
    return exchange.attributes.get(GATEWAY_ALREADY_ROUTED_ATTR) or False


def set_already_routed(exchange: ServerWebExchange):
    exchange.attributes[GATEWAY_ALREADY_ROUTED_ATTR] = True
