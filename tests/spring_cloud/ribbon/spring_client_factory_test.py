# -*- coding: utf-8 -*-

__author__ = "Ssu-Tsen"
__license__ = "Apache 2.0"

# standard library
from typing import List

# scip plugin
from ribbon.client.config.client_config import ClientConfig
from spring_cloud.ribbon.spring_client_factory import SpringClientFactory


class TestSpringClientFactory:
    service_ids = ["1", "2", "2"]
    spring_client_factory = SpringClientFactory()

    def test_get_client_config(self):
        assert isinstance(self.spring_client_factory.get_client_config(self.service_ids[0]), ClientConfig)
        assert self.spring_client_factory.get_client_config(
            self.service_ids[1]
        ) == self.spring_client_factory.get_client_config(self.service_ids[2])
