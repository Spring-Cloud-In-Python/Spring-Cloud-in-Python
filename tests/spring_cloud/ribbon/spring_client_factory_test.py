# -*- coding: utf-8 -*-

__author__ = "Ssu-Tsen"
__license__ = "Apache 2.0"

# standard library
from typing import List

# scip plugin
from ribbon.client.config.client_config import ClientConfig
from ribbon.loadbalancer.base_loadbalancer import BaseLoadBalancer
from ribbon.loadbalancer.loadbalancer import LoadBalancer
from spring_cloud.ribbon.spring_client_factory import DynamicServerListLoadBalancer, SpringClientFactory


class TestSpringClientFactory:

    spring_client_factory = SpringClientFactory()

    def test_get_client_config(self):
        assert isinstance(self.spring_client_factory.get_client_config("1"), ClientConfig)
        assert self.spring_client_factory.get_client_config("2") == self.spring_client_factory.get_client_config("2")

    def test_get_load_balancer(self):
        assert isinstance(self.spring_client_factory.get_load_balancer("1"), LoadBalancer)
        assert isinstance(self.spring_client_factory.get_load_balancer("1"), DynamicServerListLoadBalancer)
        assert self.spring_client_factory.get_load_balancer("2") == self.spring_client_factory.get_load_balancer("2")
