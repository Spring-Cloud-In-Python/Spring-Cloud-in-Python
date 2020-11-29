# -*- coding: utf-8 -*-

# standard library
from abc import ABC, abstractmethod

# scip plugin
from eureka.client.app_info import InstanceInfo
from ribbon.loadbalancer.loadbalancer import LoadBalancer
from ribbon.loadbalancer.server import Server
from spring_cloud.commons.client import ServiceInstance
from spring_cloud.commons.client.loadbalancer import LoadBalancerClient
from spring_cloud.ribbon.ribbon_server import RibbonServer


class DiscoveryEnabledServer(object):
    pass


class RibbonLoadBalancerClient(LoadBalancerClient):
    def __init__(self, client_factory):
        self.__client_factory = client_factory

    def choose(self, service_id: str, hint: object) -> ServiceInstance:
        """
        Select a server using a 'key'.
        :param service_id: (str)
        :return: (ServiceInstance)
        """
        server = self.get_server(self.get_load_balancer(service_id), hint)
        if not server:
            return None
        return RibbonServer(service_id, server, self.is_secure(server))

    def is_secure(self, server):
        if isinstance(server, DiscoveryEnabledServer):
            return server.get_instance_info().is_port_enabled(InstanceInfo.PortType.SECURE)
        return server.get_port() in [443, 8443]

    def get_server(self, load_balancer: LoadBalancer, hint: object) -> Server:
        if not load_balancer:
            return None
        if not hint:
            hint = "default"
        return load_balancer.choose_server(hint)

    def get_load_balancer(self, service_id: str):
        return self.__client_factory.get_load_balancer(service_id)
