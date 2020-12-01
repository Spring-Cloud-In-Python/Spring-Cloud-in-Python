# -*- coding: utf-8 -*-

__author__ = "MJ (tsngmj@gmail.com)"
__license__ = "Apache 2.0"

# scip plugin
from ribbon.client import default_client_config
from ribbon.client.client_config import ClientConfig
from ribbon.client.common_client_config_key import CommonClientConfigKey
from ribbon.client.default_client_config import DefaultClientConfig
from ribbon.eureka.discovery_enabled_server import DiscoveryEnabledServer
from ribbon.loadbalancer.abstract_server_list import AbstractServerList
from spring_cloud.utils.logger import Logger

# int overridePort = DefaultClientConfigImpl.DEFAULT_PORT;


class DiscoveryEnabledNIWSServerList(AbstractServerList):
    __log = Logger()

    def __init__(self, eurekaClient, clientConfig: ClientConfig):
        self.clientName = clientConfig.get_client_name()
        self.vipAddress = clientConfig.resolve_deployment_contextbased_vip_addresses()
        self.isSecure = clientConfig.getProperty(CommonClientConfigKey.PrioritizeVipAddressBasedServers)
        self.overridePort = DefaultClientConfig.DEFAULT_PORT
        self.prioritizeVipAddressBasedServers = True
        self.shouldUseOverridePort = False
        self.shouldUseIpAddr = False

        # if part not done

        pass

    @staticmethod
    def __create_client_config(self):
        clientConfig = default_client_config.getClientConfigWithDefaultValues()
        return clientConfig

    def get_initial_list_of_servers(self) -> DiscoveryEnabledServer:
        return self.obtain_servers_via_discovery()

    def get_updated_list_of_servers(self) -> DiscoveryEnabledServer:
        return self.obtain_servers_via_discovery()

    def obtain_servers_via_discovery(self) -> DiscoveryEnabledServer:
        pass
