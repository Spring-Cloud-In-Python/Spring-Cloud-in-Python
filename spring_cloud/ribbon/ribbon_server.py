# -*- coding: utf-8 -*-

__author__ = "Ssu-Tsen"
__license__ = "Apache 2.0"

from typing import Set

class RibbonServer(ServerInstance):
    def __init__(self, service_id, server, secure, metadata):
        self.__service_id = service_id
        self.__server = server
        self.__secure = secure
        self.__metadata = metadata

    def get_instance_id(self):
        return self.__server.get_id()

    def get_service_id(self):
        return self.__service_id

    def get_host(self):
        return self.__server.get_host()

    def get_port(self):
        return self.__server.get_port()

    def is_secure(self):
        return self.__secure

    def get_uri(self):
        return DefaultServiceInstance.getUri(self)

    def get_metadata(self) -> dict[str, str]:
        return self.__metadata

    def get_server(self):
        return self.__server

    def get_scheme(self):
        return self.__server.get_scheme()





