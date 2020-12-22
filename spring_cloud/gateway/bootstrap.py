# -*- coding: utf-8 -*-
# standard library
from http.server import HTTPServer
from typing import Callable, Optional

# scip plugin
from spring_cloud.commons.http import RestTemplate
from spring_cloud.gateway.filter.global_filter import RestTemplateRouteFilter
from spring_cloud.gateway.handler import DispatcherHandler
from spring_cloud.gateway.handler.handler import FilteringWebHandler, RoutePredicateHandlerMapping
from spring_cloud.gateway.route.builder.route_locator import RouteLocator, RouteLocatorBuilder
from spring_cloud.gateway.server.request_handler import HTTPRequestHandler
from spring_cloud.utils import logging

__author__ = "Waterball (johnny850807@gmail.com)"
__license__ = "Apache 2.0"


class ApiGatewayApplication:
    @staticmethod
    def run(
        route_locator_builder_consumer: Callable[[RouteLocatorBuilder], RouteLocator],
        host_name: Optional[str] = "0.0.0.0",
        port_: Optional[int] = 8726,
        enable_discovery_client: Optional[bool] = False,
    ):
        logger = logging.getLogger("spring_cloud.ApiGatewayApplication")
        web_server = None
        try:

            logger.info(f"Launching ApiGatewayApplication listening at {host_name}:{port_}")
            if enable_discovery_client:
                logger.info("The discovery client routing is enabled.")
                # scip plugin
                import spring_cloud.context.bootstrap_client as spring_cloud_bootstrap

                api: RestTemplate = spring_cloud_bootstrap.enable_service_discovery()
            else:
                api = RestTemplate()

            route_locator = route_locator_builder_consumer(RouteLocatorBuilder())
            logger.debug(str(route_locator))

            route_mapping = RoutePredicateHandlerMapping(route_locator)
            filtering_web_handler = FilteringWebHandler([RestTemplateRouteFilter(api)])
            dispatcher_handler = DispatcherHandler(route_mapping, filtering_web_handler)

            web_server = HTTPServer(
                (host_name, port_),
                lambda *args, **kwargs: HTTPRequestHandler(*args, dispatcher_handler=dispatcher_handler, **kwargs),
            )

            logger.info(f"Server listening at {host_name}:{port_}")

            web_server.serve_forever()
        except KeyboardInterrupt:
            pass
        except Exception as err:
            logger.error(str(err))

        if web_server:
            web_server.server_close()
            logger.info("Server stopped.")


def define_routes(route_locator_builder: RouteLocatorBuilder) -> RouteLocator:
    return (
        route_locator_builder.routes()
        .route(lambda p: p.path("/api/users/**").uri("http://localhost:10000"))
        .route(lambda p: p.path("/api/messages/**").uri("http://localhost:10001"))
        .build()
    )


if __name__ == "__main__":
    # standard library
    import os

    port = int(os.getenv("port") or 80)
    ApiGatewayApplication.run(define_routes, port_=port, enable_discovery_client=False)
