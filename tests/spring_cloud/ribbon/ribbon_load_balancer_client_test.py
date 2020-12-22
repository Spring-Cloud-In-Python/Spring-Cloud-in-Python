# -*- coding: utf-8 -*-
# standard library
from unittest.mock import Mock

__author__ = "Ssu-Tsen"
__license__ = "Apache 2.0"

# standard library
from typing import List

# scip plugin
from eureka.client.app_info import InstanceInfo, LeaseInfo
from ribbon.eureka.discovery_enabled_server import DiscoveryEnabledServer
from ribbon.loadbalancer.dynamic_server_list_load_balancer import DynamicServerListLoadBalancer
from ribbon.loadbalancer.server import Server
from spring_cloud.ribbon.ribbon_load_balancer_client import RibbonLoadBalancerClient
from spring_cloud.ribbon.ribbon_server import RibbonServer
from spring_cloud.ribbon.spring_client_factory import SpringClientFactory
from tests.eureka.client.discovery.shared.stubs import instance_info


class FakeEurekaClient:
    def get_instances_by_virtual_host_name(self, a=None, b=None):
        info1 = instance_info(port=100)
        info2 = instance_info(port=200)
        info3 = instance_info(port=300)

        return [info1, info2, info3]


eureka_client = Mock()
server_with_wrong_port = Server(host="127.0.0.1", port=56747, scheme="https")
server_with_right_port = Server(host="127.0.0.1", port=443, scheme="https")
spring_client_factory = SpringClientFactory(eureka_client)
ribbon_load_balancer_client = RibbonLoadBalancerClient(spring_client_factory)
ribbon_server = RibbonServer(service_id="1", server=server_with_right_port, secure=True)
discovery_enable_server = DiscoveryEnabledServer(instance_info())
lb = DynamicServerListLoadBalancer()
lb.server_list.vip_addresses = "127.0.0.1"
lb.server_list.eureka_client = FakeEurekaClient()
lb.update_list_of_servers()


def test_is_secure_when_discovery_enabled_server():
    assert ribbon_load_balancer_client.is_secure(discovery_enable_server, "1") == False


def test_is_secure_by_checking_wrong_port():
    assert ribbon_load_balancer_client.is_secure(server_with_wrong_port, "1") == False


def test_is_secure_by_checking_right_port():
    assert ribbon_load_balancer_client.is_secure(server_with_right_port, "1") == True


def test_get_server_by_load_balancer():
    assert isinstance(ribbon_load_balancer_client.get_server(lb), Server)
