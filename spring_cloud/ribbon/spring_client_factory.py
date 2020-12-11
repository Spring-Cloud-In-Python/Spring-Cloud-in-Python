# -*- coding: utf-8 -*-

__author__ = "Ssu-Tsen"
__license__ = "Apache 2.0"

# standard library
from typing import Dict

# scip plugin
from ribbon.client.config.client_config import ClientConfig
from ribbon.loadbalancer.base_loadbalancer import BaseLoadBalancer


class DynamicServerListLoadBalancer(BaseLoadBalancer):
    # TODO: it is a class from Ribbon
    pass


class SpringClientFactory:
    def __init__(
        self,
        client_configs: Dict[str, ClientConfig] = {},
        load_balancers: Dict[str, DynamicServerListLoadBalancer] = {},
    ):
        self.__client_configs = client_configs
        self.__load_balancers = load_balancers

    def get_client_config(self, service_id: str) -> ClientConfig:
        if service_id not in self.__client_configs.keys():
            self.__create_client_config(service_id)

        return self.__client_configs[service_id]

    def get_load_balancer(self, service_id: str) -> DynamicServerListLoadBalancer:
        if service_id not in self.__load_balancers.keys():
            self.__create_load_balancer(service_id)

        return self.__load_balancers[service_id]

    def __create_client_config(self, service_id: str):
        config = ClientConfig()
        config.load_default_values()
        config.add_property("service_id", service_id)
        self.__client_configs[service_id] = config

    def __create_load_balancer(self, service_id: str):
        dynamic_load_balancer = DynamicServerListLoadBalancer()
        self.__load_balancers[service_id] = dynamic_load_balancer
