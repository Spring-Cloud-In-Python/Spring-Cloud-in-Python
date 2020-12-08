# -*- coding: utf-8 -*-

__author__ = "MJ (tsngmj@gmail.com)"
__license__ = "Apache 2.0"

# scip plugin
from ribbon.client.config.client_config import ClientConfig
from ribbon.loadbalancer.base_loadbalancer import BaseLoadBalancer
from ribbon.loadbalancer.server import Server


def test_init_without_given_any_params():
    lb = BaseLoadBalancer()

    assert lb.name == "LoadBalancer"
    assert lb.rule.loadbalancer is None
    assert lb.server_list == []
    assert lb.counter == 0


def test_init_with_given_config():
    config = ClientConfig()
    config.add_property("ClientName", "MJ_is_awesome")
    config.add_property("NFLoadBalancerPingInterval", 100)
    config.add_property("NFLoadBalancerMaxTotalPingTime", 200)

    lb = BaseLoadBalancer(config=config)

    assert lb.name == "MJ_is_awesome"
    assert lb._ping_interval_time_in_sec == 100
    assert lb._max_total_ping_time_in_sec == 200


def test_choose_a_server_with_given_three_alive_server():
    server1 = Server(uri="http://127.0.0.1:100")
    server2 = Server(uri="http://127.0.0.1:200")
    server3 = Server(uri="http://127.0.0.1:300")

    servers = [server1, server2, server3]
    lb = BaseLoadBalancer()
    lb.add_servers(servers)

    assert len(lb.get_reachable_servers()) == 3
    assert lb.choose_server("uselessKey").port == 200
    assert lb.choose_server("uselessKey").port == 300


def test_choose_a_server_with_given_two_alive_and_one_not_alive_server():
    server1 = Server(uri="http://127.0.0.1:100")
    server2 = Server(uri="http://127.0.0.1:200")
    server3 = Server(uri="http://127.0.0.1:300")

    servers = [server1, server2, server3]
    lb = BaseLoadBalancer()
    lb.add_servers(servers)

    lb.mark_server_down(server3)

    assert len(lb.get_reachable_servers()) == 2
    assert lb.choose_server("uselessKey").port == 200
    assert lb.choose_server("uselessKey").port == 100
