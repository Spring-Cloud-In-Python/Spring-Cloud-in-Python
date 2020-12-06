# -*- coding: utf-8 -*-

__author__ = "Ssu-Tsen"
__license__ = "Apache 2.0"

# scip plugin
from eureka.client.app_info import InstanceInfo, LeaseInfo
from ribbon.client.config.client_config import ClientConfig
from ribbon.eureka.discovery_enabled_server import DiscoveryEnabledServer
from ribbon.loadbalancer.server import Server
from spring_cloud.ribbon.ribbon_load_balancer_client import RibbonLoadBalancerClient
from spring_cloud.ribbon.ribbon_server import RibbonServer

server_ = Server(host="127.0.0.1", port=56747, scheme="https")


class LoadBalancer:
    def choose_server(self, hint=None) -> Server:
        return server_


load_balancer1 = LoadBalancer()
load_balancer2 = LoadBalancer()
client_config1 = ClientConfig()
client_config2 = ClientConfig()
load_balancers = {"1": load_balancer1, "2": load_balancer2}
client_configs = {"1": client_config1, "2": client_config2}
ribbon_load_balancer_client = RibbonLoadBalancerClient(load_balancers=load_balancers, client_configs=client_configs)
ribbon_server = RibbonServer(service_id="1", server=server_, secure=True)
instance_info = InstanceInfo(
    instance_id="instance_id",
    app_name="app_name",
    app_group_name="app_group_name",
    ip_address="127.0.0.1",
    vip_address="stub-service",
    secure_vip_address="stub-service",
    lease_info=LeaseInfo(),
    metadata={},
    host_name="localhost",
)
discovery_enable_server = DiscoveryEnabledServer(instance_info)


def test_get_server():
    lb = LoadBalancer()
    assert ribbon_load_balancer_client.get_server(lb) == server_


def test_get_load_balancer():
    assert ribbon_load_balancer_client.get_load_balancer("1") == load_balancers["1"]


def test_is_secure_when_config():
    assert ribbon_load_balancer_client.is_secure(server_, "1") == True


def test_is_secure_when_discovery_enabled_server():
    assert ribbon_load_balancer_client.is_secure(server=discovery_enable_server, service_id="1") == False


def test_choose():
    assert ribbon_server == ribbon_load_balancer_client.choose("1")
