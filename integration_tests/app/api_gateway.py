# -*- coding: utf-8 -*-
# scip plugin
from spring_cloud.gateway.bootstrap import ApiGatewayApplication
from spring_cloud.gateway.filter import GatewayFilter, GatewayFilterChain
from spring_cloud.gateway.route.builder.route_locator import RouteLocator, RouteLocatorBuilder
from spring_cloud.gateway.server import ServerWebExchange
from spring_cloud.utils import logging

__author__ = "Waterball (johnny850807@gmail.com)"
__license__ = "Apache 2.0"

logger = logging.getLogger("api_gateway")


class MyFilter(GatewayFilter):
    def filter(self, exchange: ServerWebExchange, chain: GatewayFilterChain) -> None:
        logger.info(f"Forwarding the request uri={exchange.request.uri}")
        return chain.filter(exchange)

    def __str__(self):
        return "[MyFilter]"


def define_routes(route_locator_builder: RouteLocatorBuilder) -> RouteLocator:
    user_service_base_url = os.getenv("user-service-base-url")
    message_service_base_url = os.getenv("message-service-base-url")
    logger.debug(f"user-service-base-url: {user_service_base_url}")
    logger.debug(f"message-service-base-url: {message_service_base_url}")
    return (
        route_locator_builder.routes()
        .route(lambda p: p.path("/api/users/**").filters(lambda f: f.filter(MyFilter())).uri(user_service_base_url))
        .route(lambda p: p.path("/api/messages/**").uri(message_service_base_url))
        .build()
    )


if __name__ == "__main__":
    # standard library
    import os

    port = int(os.getenv("port") or 80)
    enable_discovery_client = bool(os.getenv("enable-discovery-client"))
    eureka_server_url: str = os.getenv("eureka-server-url")
    logger.debug(f"enable-discovery-client: {enable_discovery_client}")
    logger.debug(f"eureka-server-url: {eureka_server_url}")
    logger.info("Running the ApiGatewayApplication...")
    ApiGatewayApplication.run(
        define_routes,
        port_=port,
        enable_discovery_client=enable_discovery_client,
        eureka_server_urls=[eureka_server_url],
    )
