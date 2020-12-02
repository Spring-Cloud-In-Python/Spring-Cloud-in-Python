# -*- coding: utf-8 -*-

__author__ = "MJ (tsngmj@gmail.com)"
__license__ = "Apache 2.0"

# standard library
from typing import List

# scip plugin
from eureka.client.app_info import InstanceInfo
from ribbon.client.config.client_config import ClientConfig
from ribbon.eureka.discovery_enabled_server import DiscoveryEnabledServer
from ribbon.loadbalancer.server import Server
from ribbon.loadbalancer.server_list import ServerList
from ribbon.loadbalancer.server_list_filter import ServerListFilter


class DiscoveryEnabledNIWSServerList(ServerList):
    def __init__(self, eureka_client=None, vip_addresses: str = None, client_config: ClientConfig = None):
        self.__eureka_client = eureka_client
        self.__vip_addresses = self.__split_vip_addresses(vip_addresses)
        self.__client_config = client_config or self._create_client_config()
        self.__client_name = self.__client_config.get_property("CLIENT_NAME")
        self.__is_secure = self.__client_config.get_property("IS_SECURE")
        self.__override_port = self.__client_config.get_property("PORT")
        self.__prioritize_vip_address_based_servers = self.__client_config.get_property(
            "PRIORITIZE_VIP_ADDRESS_BASED_SERVERS"
        )
        self._should_use_ip_address = self.__client_config.get_property("USE_IPADDRESS_FOR_SERVER")

        if bool(self.__client_config.get_property("FORCE_CLIENT_PORT_CONFIGURATION")) and self.isSecure:
            self.should_use_override_port = True
        else:
            self.should_use_override_port = False

    @staticmethod
    def _create_client_config():
        client_config = ClientConfig()
        client_config.load_default_values()
        return client_config

    @property
    def eureka_client(self):
        return self.__eureka_client

    @property
    def vip_addresses(self) -> List[str]:
        return self.__vip_addresses

    @vip_addresses.setter
    def vip_addresses(self, vip_addresses: str):
        self.__vip_addresses = self.__split_vip_addresses(vip_addresses)

    @property
    def filter(self):
        """
        Not implement for minimum version
        """
        return None

    @filter.setter
    def filter(self):
        """
        Not implement for minimum version
        """
        pass

    @property
    def initial_list_of_servers(self) -> DiscoveryEnabledServer:
        return self.obtain_servers_via_discovery

    @property
    def updated_list_of_servers(self) -> DiscoveryEnabledServer:
        return self.obtain_servers_via_discovery

    @property
    def obtain_servers_via_discovery(self) -> List[Server]:
        server_list: List[Server] = []

        if self.__vip_addresses and self.__eureka_client:
            for vip_address in self.__vip_addresses:
                instance_info_list: List[InstanceInfo] = self.__eureka_client.get_instances_by_vip_address(
                    vip_address, self.__is_secure
                )
                server_list = self.__extract_server_list(instance_info_list)

                if len(server_list) and bool(self.__prioritize_vip_address_based_servers):
                    break

        return server_list

    def __extract_server_list(self, instance_info_list):
        server_list: List[Server] = []
        for instance_info in instance_info_list:
            if instance_info.status is InstanceInfo.Status.UP:
                instance_info = self.__set_instance_info_port(instance_info)
                des: DiscoveryEnabledServer = self._create_server(
                    instance_info, self.__is_secure, self._should_use_ip_address
                )

                server_list.append(des)

        return server_list

    def __set_instance_info_port(self, instance_info):
        if self.should_use_override_port:
            if self.__is_secure:
                instance_info.secure_port = self.__override_port
            else:
                instance_info.port = self.__override_port

        return instance_info

    @staticmethod
    def __split_vip_addresses(vip_addresses: str):
        if vip_addresses:
            return vip_addresses.strip().replace(" ", "").split(",")
        else:
            return []

    @staticmethod
    def _create_server(
        instance_info: InstanceInfo, is_secure: str, should_use_ip_address: str
    ) -> DiscoveryEnabledServer:
        server: DiscoveryEnabledServer = DiscoveryEnabledServer(
            instance_info, bool(is_secure), bool(should_use_ip_address)
        )

        return server

    def __str__(self):
        msg = (
            f"DiscoveryEnabledNIWSServerList: \n"
            f"ClientName: {self.__client_config}\n"
            f"Effective vipAddresses: {self.__vip_addresses}\n"
            f"IsSecure: {self.__is_secure}\n"
        )

        return msg
