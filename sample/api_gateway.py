# -*- coding: utf-8 -*-
# standard library
import time

# scip plugin
from spring_cloud.gateway.bootstrap import ApiGatewayApplication
from spring_cloud.gateway.filter import GatewayFilter, GatewayFilterChain
from spring_cloud.gateway.route.builder.route_locator import RouteLocator, RouteLocatorBuilder
from spring_cloud.gateway.server import ServerWebExchange
from spring_cloud.utils import logging

__author__ = "Waterball (johnny850807@gmail.com)"
__license__ = "Apache 2.0"

logger = logging.getLogger("api_gateway")


def define_routes(route_locator_builder: RouteLocatorBuilder) -> RouteLocator:
    return route_locator_builder.routes().route(lambda p: p.path("/api/sum/**").uri("http://sum-service")).build()


if __name__ == "__main__":
    # standard library
    import os

    time.sleep(3)
    port = int(os.getenv("port") or 80)
    eureka_server_url: str = os.getenv("eureka-server-url")
    logger.info(f"eureka-server-url: {eureka_server_url}")
    logger.info("Running the ApiGatewayApplication...")
    ApiGatewayApplication.run(
        define_routes, port_=port, enable_discovery_client=True, eureka_server_urls=[eureka_server_url],
    )
