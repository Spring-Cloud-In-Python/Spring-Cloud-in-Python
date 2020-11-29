# -*- coding: utf-8 -*-

__author__ = "Ssu-Tsen"
__license__ = "Apache 2.0"


# standard library
from typing import Set

# scip plugin
from ribbon.loadbalancer.server import Server
from spring_cloud.commons.client import ServiceInstance


class RibbonServer(ServiceInstance):
    def __init__(self, service_id: str, server: Server, secure: bool):
        self.__service_id = service_id
        self.__server = server
        self.__secure = secure

    def instance_id(self) -> str:
        return self.__server.get_id()

    def service_id(self) -> str:
        return self.__service_id

    def host(self) -> str:
        return self.__server.get_host()

    def port(self) -> int:
        return self.__server.get_port()

    def secure(self) -> bool:
        return self.__secure

    def uri(self) -> str:
        scheme = "https" if self.secure else "http"
        uri = "{}://{}{}".format(scheme, self.host(), self.port())
        return uri

    def server(self) -> Server:
        return self.__server

    def scheme(self) -> str:
        return self.__server.get_scheme(self.uri())
