# -*- coding: utf-8 -*-

__author__ = "MJ (tsngmj@gmail.com)"
__license__ = "Apache 2.0"

# scip plugin
from ribbon.client.config.client_config import ClientConfig
from ribbon.eureka.discovery_enabled_niws_server_list import DiscoveryEnabledNIWSServerList
from ribbon.loadbalancer.base_load_balancer import BaseLoadBalancer
from ribbon.loadbalancer.load_balance_rule import LoadBalanceRule
from ribbon.loadbalancer.server import Server
from ribbon.loadbalancer.server_list import ServerList


class DynamicServerListLoadBalancer(BaseLoadBalancer):
    def __init__(
        self,
        name: str = None,
        rule: LoadBalanceRule = None,
        config: ClientConfig = None,
        server_list: ServerList = None,
    ):
        super(DynamicServerListLoadBalancer, self).__init__(name, rule, config)
        self.__server_list = server_list or DiscoveryEnabledNIWSServerList(client_config=config)

        self.update_list_of_servers()

    def choose_server(self, key: object) -> Server:
        self.update_list_of_servers()
        return super(DynamicServerListLoadBalancer, self).choose_server(key=key)

    def update_list_of_servers(self):
        if self.__server_list:
            servers = self.__server_list.updated_list_of_servers

            for server in servers:
                server.is_alive = True

        self.servers = servers

    @property
    def server_list(self):
        return self.__server_list

    @server_list.setter
    def server_list(self, server_list):
        self.__server_list = server_list
