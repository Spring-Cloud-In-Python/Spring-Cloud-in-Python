# -*- coding: utf-8 -*-

__author__ = "MJ (tsngmj@gmail.com)"
__license__ = "Apache 2.0"

# scip plugin
from ribbon.eureka.discovery_enabled_niws_server_list import DiscoveryEnabledNIWSServerList


def test_init_without_given_any_params():
    server_list = DiscoveryEnabledNIWSServerList()

    assert server_list.vip_addresses is None
    assert server_list.obtain_servers_via_discovery == []
    # assert se
