# -*- coding: utf-8 -*-

__author__ = "MJ (tsngmj@gmail.com)"
__license__ = "Apache 2.0"

# standard library
from abc import ABC, abstractmethod


class Server:
    class MetaInfo(ABC):
        @classmethod
        @abstractmethod
        def get_app_name(cls) -> str:
            """
            :return: str, the name of application that runs on this server, null if not available
            """
            pass

        @classmethod
        @abstractmethod
        def get_server_group(cls) -> str:
            """
            :return: str, the group of the server, for example, auto scaling group ID in AWS.
            """
            pass

        @classmethod
        @abstractmethod
        def get_service_id_for_discovery(cls) -> str:
            """
            :return: str, a virtual address used by the server to register with discovery service.
            """
            pass

        @classmethod
        @abstractmethod
        def get_instance_id(cls) -> str:
            """
            :return: str, ID of the server
            """
            pass

    class __SimpleMetaInfo(MetaInfo):
        def get_app_name(cls) -> str:
            return None

        def get_server_group(cls) -> str:
            return None

        def get_service_id_for_discovery(cls) -> str:
            return None

        def get_instance_id(cls) -> str:
            return cls.__id

    UNKNOWN_ZONE = "UNKNOWN"
    # actually it should be public and final, but here is only public not final

    def __init__(self, id: str = None):
        self.set_id(id)
        self.__isFlagAlive = False
        self.__readyToServe = True
        self.__zone = self.UNKNOWN_ZONE

    @classmethod
    def normalize_id(cls, id: str) -> str:
        hostPort = cls.get_host_port(id)

        if hostPort is None:
            return None

        return hostPort[0] + ":" + str(hostPort[1])

    @classmethod
    def __get_scheme(cls, id: str) -> str:
        if id is None:
            return None

        scheme = None
        if id.lower().startswith("http://"):
            scheme = "http"
        elif id.lower().startswith("https://"):
            scheme = "https"

        return scheme

    @classmethod
    def get_host_port(cls, id: str) -> tuple:
        if id is None:
            return None

        host = ""
        port = 80

        if id.lower().startswith("http://"):
            id = id[7:]
        elif id.lower().startswith("https://"):
            id = id[8:]
            port = 443

        if "/" in id:
            index = id.find("/")
            id = id[0:index]

        colonIndex = id.find(":")

        if colonIndex == -1:
            host = id
        else:
            host = id[0:colonIndex]
            try:
                port = int(id[colonIndex + 1 :])
            except ValueError as err:
                raise err

        return (host, port)

    def set_host(self, host: str):
        if host != None:
            self.__host = host
            self.__id = host + ":" + str(self.__port)

    def set_port(self, port: int):
        self.__port = port
        if self.__host != None:
            self.__id = self.__host + ":" + str(port)

    def set_zone(self, zone: str):
        self.__zone = zone

    def set_scheme(self, scheme: str):
        self.__scheme = scheme

    def set_id(self, id: str):
        print(id)
        hostPort = self.get_host_port(id)

        print(hostPort)
        if hostPort is None:
            self.__id = None
        else:
            self.__id = hostPort[0] + ":" + str(hostPort[1])
            self.__host = hostPort[0]
            self.__port = hostPort[1]
            self.__scheme = self.__get_scheme(id)

    def set_ready_to_serve(self, ready_to_serve: bool):
        self.__readyToServe = ready_to_serve

    def get_host(self) -> str:
        return self.__host

    def get_port(self) -> int:
        return self.__port

    def get_zone(self) -> str:
        return self.__zone

    def get_id(self) -> str:
        return self.__id

    def get_meta_info(self) -> MetaInfo:
        return self.__simple_meta_info

    def is_ready_to_serve(self) -> bool:
        return self.__readyToServe

    def is_alive(self) -> bool:
        return self.__isFlagAlive

    def equals(self, obj: object) -> bool:
        pass

    def hash_code(self) -> int:
        hash = 7
        hash = 31 * hash + (None == self.get_id() and 0 or hash(self.get_id()))

        return hash

    def to_string(self) -> str:
        return self.get_id
