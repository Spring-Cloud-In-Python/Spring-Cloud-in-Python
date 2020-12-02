# -*- coding: utf-8 -*-

__author__ = "MJ (tsngmj@gmail.com)"
__license__ = "Apache 2.0"

# scip plugin
from ribbon.eureka.discovery_enabled_server import DiscoveryEnabledServer
from tests.eureka.client.discovery.shared.stubs import instance_info


class TestDiscoveryEnabledServer:
    tmp_instance_info = instance_info()

    def test_init_with_given_instance_info_and_do_not_use_secure_port_and_in_address(self):
        server = DiscoveryEnabledServer(instance_info=self.tmp_instance_info, use_secure_port=False)

        assert server.is_alive == True
