# -*- coding: utf-8 -*-
# scip plugin
from spring_cloud.utils import logging

__author__ = "MJ (tsngmj@gmail.com)"
__license__ = "Apache 2.0"

# standard library
from typing import List

# scip plugin
from ribbon.client.config.client_config import ClientConfig
from ribbon.loadbalancer.load_balance_rule import LoadBalanceRule
from ribbon.loadbalancer.load_balancer import LoadBalancer
from ribbon.loadbalancer.round_robin_rule import RoundRobinRule
from ribbon.loadbalancer.server import Server


class BaseLoadBalancer(LoadBalancer):
    def __init__(self, name: str = None, rule: LoadBalanceRule = None, config: ClientConfig = None):
        self._logger = logging.getLogger(f"ribbon.BaseLoadBalancer({name})")
        self._name = name or "LoadBalancer"
        self._rule = rule or RoundRobinRule()
        self._servers: List[Server] = []
        self._counter = 0
        self._ping_interval_time_in_sec = 10
        self._max_total_ping_time_in_sec = 5

        if config:
            self._name = config.get_property("ClientName")
            self._ping_interval_time_in_sec = config.get_property("NFLoadBalancerPingInterval")
            self._max_total_ping_time_in_sec = config.get_property("NFLoadBalancerMaxTotalPingTime")

    def add_server(self, server: Server = None):
        """
        Todo: Minimum version assume all server is alive when first add into the list
        """
        if server:
            server.is_alive = True
            self._servers.append(server)

    def add_servers(self, servers: List[Server] = None):
        """
        Todo: Minimum version assume all server is alive when first add into the list
        """
        if servers:
            for server in servers:
                server.is_alive = True

            self._servers.extend(servers)

    def choose_server(self, key: object) -> Server:
        if self._rule.loadbalancer is None:
            self._rule.loadbalancer = self
        self._logger.info(f"Use **{self._rule}** to choose a server to send the request to.")
        server = self._rule.choose(key=key)
        self._logger.info(f"Successfully load-balancing with the selected server: {server.host}:{server.port}.")
        return server

    def mark_server_down(self, server: Server):
        if server:
            server.is_alive = False

    def get_reachable_servers(self) -> List[Server]:
        return [server for server in self._servers if server.is_alive]

    def get_all_servers(self) -> List[Server]:
        return self._servers

    @property
    def client_config(self):
        return self._client_config

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @property
    def rule(self):
        return self._rule

    @rule.setter
    def rule(self, rule):
        self._rule = rule

    @property
    def servers(self):
        return self._servers

    @servers.setter
    def servers(self, servers: List[Server]):
        """
        Todo: Minimum version assume all server is alive when first add into the list
        """
        for server in servers:
            server.is_alive = True

        self._servers = servers

    @property
    def counter(self):
        return self._counter
