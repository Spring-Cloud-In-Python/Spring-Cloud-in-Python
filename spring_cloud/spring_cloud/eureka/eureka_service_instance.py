# -*- coding: utf-8 -*-

__author__ = "Ricky"
__license__ = "Apache 2.0"

# scip plugin

# scip plugin
from spring_cloud.commons.client.service_instance import ServiceInstance
from tests.spring_cloud.eureka.instanceinfo import InstanceInfo


class EurekaServiceInstance(ServiceInstance):
    def __init__(self, instance_info: InstanceInfo):
        assert instance_info, "instance_info cannot be null"
        self.__instance = instance_info

    def get_instance_info(self) -> InstanceInfo:
        return self.__instance

    def instance_id(self) -> str:
        return self.__instance.get_id()

    def service_id(self) -> str:
        return self.__instance.get_app_name()

    def host(self) -> str:
        return self.__instance.get_host_name()

    def port(self) -> int:
        if self.secure():
            return self.__instance.get_secure_port()
        return self.__instance.get_port()

    def secure(self) -> bool:
        return self.__instance.is_port_enabled("SECURE")

    def uri(self) -> str:
        if self.secure():
            scheme = "https"
        else:
            scheme = "http"
        uri = "{}://{}:{}".format(scheme, self.host(), self.port())
        return uri

    def scheme(self) -> str:
        return self.uri().split(":")[0]

    def __eq__(self, obj) -> bool:
        if obj is self:
            return True
        if not obj or self.__class__ != obj.__class__:
            return False
        return self.__instance == obj.__instance

    def __hash__(self) -> int:
        return hash(self.__instance)
