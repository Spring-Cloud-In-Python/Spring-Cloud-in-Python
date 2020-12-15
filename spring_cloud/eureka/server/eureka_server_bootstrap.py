# -*- coding: utf-8 -*-

__author__ = "Ricky"
__license__ = "Apache 2.0"

# standard library
from typing import Optional

# pypi/conda library
import uvicorn

# scip plugin
from eureka.server.discovery_server import UvicornDiscoveryServer


class EurekaServerBootstrap:
    def __init__(self):
        self.__discovery_server = UvicornDiscoveryServer()

    def run(self, host: Optional[str] = "0.0.0.0", port: Optional[int] = 8787):
        self.__discovery_server.initialize()
        self.__discovery_server.run(host=host, port=port)


if __name__ == "__main__":
    EurekaServerBootstrap().run()
