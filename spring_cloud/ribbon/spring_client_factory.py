# -*- coding: utf-8 -*-
# scip plugin
from eureka.client.discovery import EurekaClient
from ribbon.loadbalancer.load_balancer import LoadBalancer
from ribbon.loadbalancer.round_robin_rule import RoundRobinRule
from spring_cloud.utils import logging

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
        eureka_client: EurekaClient,
        client_configs: Dict[str, ClientConfig] = {},
        load_balancers: Dict[str, LoadBalancer] = {},
    ):
        self.logger = logging.getLogger("spring_cloud.ribbon.SpringClientFactory")
        self.eureka_client = eureka_client
        self.__client_configs = client_configs
        self.__load_balancers = load_balancers

    def get_client_config(self, service_id: str) -> ClientConfig:
        if service_id not in self.__client_configs.keys():
            self.__client_configs[service_id] = self.__create_client_config(service_id)

        return self.__client_configs[service_id]

    def get_load_balancer(self, service_id: str) -> LoadBalancer:
        if service_id not in self.__load_balancers.keys():
            self.__load_balancers[service_id] = self.__create_load_balancer(service_id)

        return self.__load_balancers[service_id]

    def __create_client_config(self, service_id: str) -> ClientConfig:
        config = ClientConfig()
        config.load_default_values()
        config.add_property("service_id", service_id)
        return config

    def __create_load_balancer(self, service_id: str) -> LoadBalancer:
        self.logger.trace("Creating Ribbon's load-balancer...")
        lb_rule = RoundRobinRule()
        client_config = self.get_client_config(service_id)
        server_list = DiscoveryEnabledNIWSServerList(
            eureka_client=self.eureka_client, vip_addresses=service_id, client_config=client_config
        )
        return DynamicServerListLoadBalancer(service_id, lb_rule, client_config, server_list)
