# -*- coding: utf-8 -*-

__author__ = "Ssu-Tsen"
__license__ = "Apache 2.0"

# standard library
from typing import Dict

# scip plugin
from ribbon.client.config.client_config import ClientConfig
from ribbon.eureka.discovery_enabled_niws_server_list import DiscoveryEnabledNIWSServerList
from ribbon.loadbalancer.dynamic_server_list_load_balancer import DynamicServerListLoadBalancer


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
        discovery_enabled_niws_server_list = DiscoveryEnabledNIWSServerList(vip_addresses=service_id)
        dynamic_load_balancer = DynamicServerListLoadBalancer(server_list=discovery_enabled_niws_server_list)
        self.__load_balancers[service_id] = dynamic_load_balancer
