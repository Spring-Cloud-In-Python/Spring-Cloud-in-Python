# -*- coding: utf-8 -*-

__author__ = "MJ (tsngmj@gmail.com)"
__license__ = "Apache 2.0"

# scip plugin
from eureka.client.app_info import InstanceInfo
from ribbon.eureka.discovery_enabled_niws_server_list import DiscoveryEnabledNIWSServerList
from ribbon.eureka.discovery_enabled_server import DiscoveryEnabledServer
from tests.eureka.client.discovery.shared.stubs import instance_info


class FakeEurekaClient:
    def get_instances_by_virtual_host_name(self, vip_address, is_secure: bool):
        return [
            instance_info(app_name="instance_1", num=1, vip_address="stub-service"),
            instance_info(app_name="instance_2", num=1, vip_address="stub-service"),
        ]


def test_init_without_given_any_params():
    server_list = DiscoveryEnabledNIWSServerList()

    assert server_list.vip_addresses == []
    assert server_list.initial_list_of_servers == []
    assert server_list.obtain_servers_via_discovery() == []


def test_init_with_given_vip_addresses():
    server_list = DiscoveryEnabledNIWSServerList(vip_addresses="127.0.0.1:80, 127.0.0.1:443 \t ")
    assert server_list.vip_addresses == ["127.0.0.1:80", "127.0.0.1:443"]


def test_init_with_fake_eureka_client():
    fake_eureka_client = FakeEurekaClient()
    server_list = DiscoveryEnabledNIWSServerList(
        eureka_client=fake_eureka_client, vip_addresses="127.0.0.1:80, 127.0.0.1:443"
    )
    target_list = server_list.obtain_servers_via_discovery()

    assert isinstance(target_list[0], DiscoveryEnabledServer)
    assert target_list[0].host == "localhost"
    assert target_list[0].port == InstanceInfo.DEFAULT_PORT
