# -*- coding: utf-8 -*-
# scip plugin
from spring_cloud.gateway.bootstrap import ApiGatewayApplication
from spring_cloud.gateway.route.builder.route_locator import RouteLocator, RouteLocatorBuilder
from spring_cloud.utils import logging

__author__ = "Waterball (johnny850807@gmail.com)"
__license__ = "Apache 2.0"

logger = logging.getLogger("api_gateway")


def define_routes(route_locator_builder: RouteLocatorBuilder) -> RouteLocator:
    puzzle_service_base_url = os.getenv("puzzle-service-base-url")
    logger.info(f"puzzle-service-base-url: {puzzle_service_base_url}")
    return (
        route_locator_builder.routes()
        .route(
            lambda p: p.path("/puzzle")
            .or_()
            .path("/answer")
            .and_()
            .not_(lambda p: p.cookie("token", "Guest-[0-9]+"))
            .filters(lambda f: f.add_request_header("identity", "user").prefix_path("/api"))
            .uri(puzzle_service_base_url)
        )
        .route(
            lambda p: p.path("/**")
            .filters(lambda f: f.add_request_header("identity", "guest").prefix_path("/api"))
            .uri(puzzle_service_base_url)
        )
        .build()
    )


if __name__ == "__main__":
    # standard library
    import os

    port = int(os.getenv("port") or 80)
    ApiGatewayApplication.run(define_routes, port_=port)
