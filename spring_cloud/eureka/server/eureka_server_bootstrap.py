# -*- coding: utf-8 -*-

__author__ = "Ricky"
__license__ = "Apache 2.0"
# pypi/conda library
import uvicorn

# scip plugin
from eureka.server.discovery_server import eureka_server, registry


class EurekaServerBootstrap:
    def __int__(self):
        self._registry = registry

    def run(self):
        uvicorn.run(eureka_server, host="0.0.0.0", port=8787)


if __name__ == "__main__":
    EurekaServerBootstrap().run()
