# -*- coding: utf-8 -*-
__author__ = "Waterball (johnny850807@gmail.com)"
__license__ = "Apache 2.0"


def define_routes(route_builder) -> RouteLocator:
    return (
        route_builder.routes()
        .route(lambda p: p.path("/api/users/**").uri("http://user-service"))
        .route(lambda p: p.path("/api/messages/**").uri("http://message-service"))
        .build()
    )


if __name__ == "__main__":
    ApiGatewayApplication.run(define_routes, enable_discovery_client=True)
