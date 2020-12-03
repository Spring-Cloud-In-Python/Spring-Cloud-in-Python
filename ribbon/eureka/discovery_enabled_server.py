# -*- coding: utf-8 -*-

__author__ = "MJ (tsngmj@gmail.com)"
__license__ = "Apache 2.0"

# scip plugin
from eureka.client.app_info import InstanceInfo
from ribbon.loadbalancer.server import MetaInfo, Server


class DiscoveryEnabledServerMetaInfo(MetaInfo):
    def __init__(self, instance_info):
        self.__instance_info = instance_info

    @classmethod
    def get_app_name(cls) -> str:
        return cls.__instance_info.app_name

    @classmethod
    def get_server_group(cls) -> str:
        return cls.__instance_info.app_group_name

    @classmethod
    def get_service_id_for_discovery(cls) -> str:
        return cls.__instance_info.vip_address

    @classmethod
    def get_instance_id(cls) -> str:
        return cls.__instance_info.instance_id


class DiscoveryEnabledServer(Server):
    def __init__(self, instance_info: InstanceInfo, use_secure_port: bool = False, use_ip_address: bool = False):
        if use_ip_address:
            super(DiscoveryEnabledServer, self).__init__(host=instance_info.ip_address, port=instance_info.port)
        else:
            super(DiscoveryEnabledServer, self).__init__(host=instance_info.host_name, port=instance_info.port)

        if use_secure_port and instance_info.is_secure_port_enabled:
            self.port = instance_info.secure_port

        self.__instance_info = instance_info
        self.__meta_info = DiscoveryEnabledServerMetaInfo(instance_info)

    @property
    def instance_info(self):
        return self.__instance_info

    @property
    def meta_info(self):
        return self.__meta_info
