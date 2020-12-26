# -*- coding: utf-8 -*-

__author__ = "Daniel1147 (sxn91401@gmail.com)"
__license__ = "Apache 2.0"

# standard library
from abc import ABC, abstractmethod
from typing import Optional

# pypi/conda library
import uvicorn

# scip plugin
from eureka.server.app import app, sole_registry
from eureka.server.server_config import DefaultServerConfig, ServerConfig


class DiscoveryServer(ABC):
    def __init__(self, server_config: Optional[ServerConfig] = DefaultServerConfig()):
        self._config = server_config

    @abstractmethod
    def initialize(self):
        pass

    @abstractmethod
    def run(self, host: Optional[str], port: Optional[int]):
        return NotImplemented


class UvicornDiscoveryServer(DiscoveryServer):
    def __init__(self, server_config: Optional[ServerConfig] = DefaultServerConfig()):
        super().__init__(server_config)
        self._registry = sole_registry
        self._app = app

    def initialize(self):
        """

        We may want to initialize the registry or synchronize with other discovery servers in the future here in the
        future.

        """
        pass

    def run(self, host: Optional[str] = None, port: Optional[int] = None):
        host = host if host is not None else self._config.host
        port = port if port is not None else self._config.port

        uvicorn.run(self._app, host=host, port=port, access_log=False)


if __name__ == "__main__":
    discovery_server = UvicornDiscoveryServer()
    discovery_server.initialize()
    discovery_server.run()
