# -*- coding: utf-8 -*-

__author__ = "MJ (tsngmj@gmail.com)"
__license__ = "Apache 2.0"

# scip plugin
from ribbon.client.config.client_config import ClientConfig
from ribbon.eureka.discovery_enabled_server import DiscoveryEnabledServer
from ribbon.loadbalancer.dynamic_server_list_load_balancer import DynamicServerListLoadBalancer
from tests.eureka.client.discovery.shared.stubs import instance_info


class FakeEurekaClient:
    def get_instances_by_virtual_host_name(self, a=None, b=None):
        info1 = instance_info(port=100)
        info2 = instance_info(port=200)
        info3 = instance_info(port=300)

        return [info1, info2, info3]


def test_init_without_given_any_params():
    lb = DynamicServerListLoadBalancer()

    assert lb.name == "LoadBalancer"
    assert lb.rule.loadbalancer is None
    assert lb.servers == []
    assert lb.counter == 0


def test_init_with_given_config():
    config = ClientConfig()
    config.load_default_values()
    config.add_property("ClientName", "MJ_is_awesome")
    config.add_property("NFLoadBalancerPingInterval", 100)
    config.add_property("NFLoadBalancerMaxTotalPingTime", 200)

    lb = DynamicServerListLoadBalancer(config=config)

    assert lb.name == "MJ_is_awesome"
    assert lb._ping_interval_time_in_sec == 100
    assert lb._max_total_ping_time_in_sec == 200


def test_choose_a_server_with_given_three_alive_server():
    lb = DynamicServerListLoadBalancer()
    lb.server_list.vip_addresses = "127.0.0.1"  # if server_list's vip_addresses is empty we won't get any server
    lb.server_list.eureka_client = FakeEurekaClient()
    lb.update_list_of_servers()

    choices = set()
    choices.add(lb.choose_server("uselessKey").port)
    choices.add(lb.choose_server("uselessKey").port)
    choices.add(lb.choose_server("uselessKey").port)

    assert len(lb.get_reachable_servers()) == 3
    assert 100 in choices
    assert 200 in choices
    assert 300 in choices

def test_choose_a_server_with_given_two_alive_and_one_not_alive_server():
    lb = DynamicServerListLoadBalancer()
    lb.server_list.vip_addresses = "127.0.0.1"  # if server_list's vip_addresses is empty we won't get any server
    lb.server_list.eureka_client = FakeEurekaClient()
    lb.update_list_of_servers()
    lb.servers[2].is_alive = False

    assert len(lb.get_reachable_servers()) == 2
