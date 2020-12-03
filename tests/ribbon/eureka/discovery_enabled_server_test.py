# -*- coding: utf-8 -*-

__author__ = "MJ (tsngmj@gmail.com)"
__license__ = "Apache 2.0"

# scip plugin
from eureka.client.app_info import InstanceInfo
from ribbon.eureka.discovery_enabled_server import DiscoveryEnabledServer
from ribbon.loadbalancer.server import MetaInfo
from tests.eureka.client.discovery.shared.stubs import instance_info


class TestDiscoveryEnabledServer:
    tmp_instance_info = instance_info()
    tmp_instance_info.is_secure_port_enabled = True

    def test_init_with_given_instance_info_and_do_not_use_secure_port_and_ip_address(self):
        server = DiscoveryEnabledServer(instance_info=self.tmp_instance_info)

        assert server.host == "localhost"
        assert server.port == InstanceInfo.DEFAULT_PORT
        assert instance_info(server.meta_info, MetaInfo)

    def test_init_with_given_instance_info_with_using_secure_port(self):
        server = DiscoveryEnabledServer(instance_info=self.tmp_instance_info, use_secure_port=True)

        assert server.port == InstanceInfo.DEFAULT_SECURE_PORT

    def test_init_with_given_instance_info_with_using_ip_address(self):
        server = DiscoveryEnabledServer(instance_info=self.tmp_instance_info, use_ip_address=True)

        assert server.host == "127.0.0.1"
