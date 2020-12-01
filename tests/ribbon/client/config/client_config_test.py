# -*- coding: utf-8 -*-

__author__ = "MJ (tsngmj@gmail.com)"
__license__ = "Apache 2.0"

# scip plugin
from ribbon.client.config.client_config import ClientConfig, DefaultClientConfig


class TestClientConfig:
    client_config = ClientConfig()

    def test_add_property_internal(self):
        self.client_config.add_property("mj", "is awesome")
        assert self.client_config.get_property("mj") == "is awesome"

    def test_get_property_internal_with_nonexistent_key(self):
        assert self.client_config.get_property("lulu") is None

    def test_delete_property(self):
        self.client_config.add_property("cat", "meow")
        self.client_config.delete_property("cat")
        assert self.client_config.get_property("cat") is None
