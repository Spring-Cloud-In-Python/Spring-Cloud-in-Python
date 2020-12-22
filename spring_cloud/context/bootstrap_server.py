# -*- coding: utf-8 -*-
# standard library

# scip plugin
from spring_cloud.eureka.server.eureka_server_bootstrap import EurekaServerBootstrap

__author__ = "Waterball (johnny850807@gmail.com)"
__license__ = "Apache 2.0"


def enable_service_registry(port=8761):
    eureka_server_bootstrap = EurekaServerBootstrap()
    eureka_server_bootstrap.run(port=port)
