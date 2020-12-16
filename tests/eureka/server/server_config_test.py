# -*- coding: utf-8 -*-

__author__ = "Daniel1147 (sxn91401@gmail.com)"
__license__ = "Apache 2.0"

# scip plugin
from eureka.server.server_config import DefaultServerConfig


class TestServerConfig:
    def test_default_server_config(self):
        default_server_config = DefaultServerConfig()
        assert default_server_config.host == "0.0.0.0"

        # Test config override.
        default_server_config.host = "127.0.0.1"
        assert default_server_config.host == "127.0.0.1"
