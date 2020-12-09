# -*- coding: utf-8 -*-

__author__ = "MJ (tsngmj@gmail.com)"
__license__ = "Apache 2.0"

# standard library
from typing import List

# scip plugin
from ribbon.client.config.client_config import ClientConfig
from ribbon.loadbalancer.loadbalance_rule import LoadBalanceRule
from ribbon.loadbalancer.loadbalancer import LoadBalancer
from ribbon.loadbalancer.roundrobin_rule import RoundRobinRule
from ribbon.loadbalancer.server import Server
from spring_cloud.utils.logging import getLogger


class BaseLoadBalancer(LoadBalancer):
    def __init__(self, name: str = None, rule: LoadBalanceRule = None, config: ClientConfig = None):
        self.__logger = getLogger()
        self.__name = name or "LoadBalancer"
        self.__rule = rule or RoundRobinRule()
        self.__servers: List[Server] = []
        self.__counter = 0
        self._ping_interval_time_in_sec = 10
        self._max_total_ping_time_in_sec = 5

        if config:
            self.__name = config.get_property("ClientName")
            self._ping_interval_time_in_sec = config.get_property("NFLoadBalancerPingInterval")
            self._max_total_ping_time_in_sec = config.get_property("NFLoadBalancerMaxTotalPingTime")

    def add_server(self, server: Server = None):
        """
        Todo: Minimum version assume all server is alive when first add into the list
        """
        if server:
            server.is_alive = True
            self.__servers.append(server)

    def add_servers(self, servers: List[Server] = None):
        """
        Todo: Minimum version assume all server is alive when first add into the list
        """
        if servers:
            for server in servers:
                server.is_alive = True
            self.__servers.extend(servers)

    def choose_server(self, key: object) -> Server:
        if self.__rule.loadbalancer is None:
            self.__rule.loadbalancer = self

        return self.__rule.choose(key=key)

    def mark_server_down(self, server: Server):
        if server:
            server.is_alive = False

    def get_reachable_servers(self) -> List[Server]:
        return [server for server in self.__servers if server.is_alive]

    def get_all_servers(self) -> List[Server]:
        return self.__servers

    @property
    def client_config(self):
        return self.__client_config

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        self.__name = name

    @property
    def rule(self):
        return self.__rule

    @rule.setter
    def rule(self, rule):
        self.__rule = rule

    @property
    def servers(self):
        return self.__servers

    @servers.setter
    def servers(self, servers: List[Server]):
        """
        Todo: Minimum version assume all server is alive when first add into the list
        """
        for server in servers:
            server.is_alive = True

        self.servers = servers

    @property
    def counter(self):
        return self.__counter
