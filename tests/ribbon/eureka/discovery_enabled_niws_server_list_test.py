# -*- coding: utf-8 -*-

__author__ = "MJ (tsngmj@gmail.com)"
__license__ = "Apache 2.0"

# scip plugin
from eureka.client.app_info import InstanceInfo, LeaseInfo
from ribbon.eureka.discovery_enabled_niws_server_list import DiscoveryEnabledNIWSServerList
from ribbon.eureka.discovery_enabled_server import DiscoveryEnabledServer


class FakeEurekaClient:
    def get_instances_by_vip_address(self, vip_address, is_secure: bool):
        if vip_address == "127.0.0.1:80":
            return [
                InstanceInfo(
                    instance_id="instance_1",
                    app_name="instance_1",
                    ip_address="127.0.0.1:80",
                    vip_address="9527",
                    secure_vip_address="127.0.0.1:443",
                    secure_port="443",
                    lease_info=LeaseInfo,
                    host_name="127.0.0.1",
                ),
                InstanceInfo(
                    instance_id="instance_2",
                    app_name="instance_2",
                    ip_address="127.0.0.1:80",
                    vip_address="9527",
                    secure_vip_address="127.0.0.1:443",
                    secure_port="443",
                    lease_info=LeaseInfo,
                    host_name="127.0.0.1",
                ),
            ]

        elif vip_address == "127.0.0.1:443":
            return [
                InstanceInfo(
                    instance_id="instance_3",
                    app_name="instance_3",
                    ip_address="127.0.0.1:80",
                    vip_address="9527",
                    secure_vip_address="127.0.0.1:443",
                    secure_port="443",
                    lease_info=LeaseInfo,
                    host_name="127.0.0.1",
                ),
                InstanceInfo(
                    instance_id="instance_4",
                    app_name="instance_4",
                    ip_address="127.0.0.1:80",
                    vip_address="9527",
                    secure_vip_address="127.0.0.1:443",
                    secure_port="443",
                    lease_info=LeaseInfo,
                    host_name="127.0.0.1",
                ),
            ]

        else:
            return []


def test_init_without_given_any_params():
    server_list = DiscoveryEnabledNIWSServerList()

    assert server_list.vip_addresses == []
    assert server_list.initial_list_of_servers == []
    assert server_list.obtain_servers_via_discovery == []


def test_init_with_given_vip_addresses():
    server_list = DiscoveryEnabledNIWSServerList(vip_addresses="127.0.0.1:80, 127.0.0.1:443 \t ")
    assert server_list.vip_addresses == ["127.0.0.1:80", "127.0.0.1:443"]


def test_init_with_fake_eureka_client():
    fake_eureka_client = FakeEurekaClient()
    server_list = DiscoveryEnabledNIWSServerList(
        eureka_client=fake_eureka_client, vip_addresses="127.0.0.1:80, 127.0.0.1:443"
    )
    target_list = server_list.obtain_servers_via_discovery
    assert isinstance(target_list[0], DiscoveryEnabledServer)
