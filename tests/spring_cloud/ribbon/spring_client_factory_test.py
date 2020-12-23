# -*- coding: utf-8 -*-
# standard library
from unittest.mock import Mock

__author__ = "Ssu-Tsen"
__license__ = "Apache 2.0"

# standard library

# scip plugin
from ribbon.client.config.client_config import ClientConfig
from spring_cloud.ribbon.spring_client_factory import DynamicServerListLoadBalancer, SpringClientFactory


class TestSpringClientFactory:
    eureka_client = Mock()
    eureka_client.get_instances_by_virtual_host_name = Mock(return_value=[])
    spring_client_factory = SpringClientFactory(eureka_client)

    def test_get_client_config(self):
        assert isinstance(self.spring_client_factory.get_client_config("1"), ClientConfig)
        assert self.spring_client_factory.get_client_config("2") == self.spring_client_factory.get_client_config("2")

    def test_get_load_balancer(self):
        assert isinstance(self.spring_client_factory.get_load_balancer("1"), DynamicServerListLoadBalancer)
        assert self.spring_client_factory.get_load_balancer("2") == self.spring_client_factory.get_load_balancer("2")
