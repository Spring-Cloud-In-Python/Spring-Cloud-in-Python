# -*- coding: utf-8 -*-

__author__ = "Waterball (johnny850807@gmail.com)"
__license__ = "Apache 2.0"


# TODO Fake, should be substituted with the real implementation
class ApiGatewayApplication:
    @staticmethod
    def run(*args, **kwargs):
        # standard library
        import time

        while True:
            time.sleep(3)
            print("Tick...")  # simulate service' running


def define_routes(route_builder):
    return (
        route_builder.routes()
        .route(lambda p: p.path("/api/users/**").uri("http://user-service"))
        .route(lambda p: p.path("/api/messages/**").uri("http://message-service"))
        .build()
    )


if __name__ == "__main__":
    # standard library
    import os

    port = int(os.getenv("port") or 80)
    ApiGatewayApplication.run(define_routes, port=port, enable_discovery_client=True)
