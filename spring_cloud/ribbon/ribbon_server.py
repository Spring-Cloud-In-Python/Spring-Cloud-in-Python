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

    @property
    def instance_id(self) -> str:
        return self.__server.id

    @property
    def service_id(self) -> str:
        return self.__service_id

    @property
    def host(self) -> str:
        return self.__server.host

    @property
    def port(self) -> int:
        return self.__server.port

    @property
    def secure(self) -> bool:
        return self.__secure

    @property
    def uri(self) -> str:
        scheme = "https" if self.secure else "http"
        uri = "{}://{}{}".format(scheme, self.host, self.port)
        return uri

    @property
    def server(self) -> Server:
        return self.__server

    @property
    def scheme(self) -> str:
        return self.__server.scheme

    def __eq__(self, o):
        if isinstance(o, RibbonServer):
            return (
                self.uri == o.uri
                and self.service_id == o.service_id
                and self.instance_id == o.instance_id
                and self.host == o.host
                and self.port == o.port
                and self.secure == o.secure
                and self.scheme == o.scheme
                and self.server == o.server
            )

        return False
