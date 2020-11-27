# -*- coding: utf-8 -*-

__author__ = "MJ (tsngmj@gmail.com)"
__license__ = "Apache 2.0"

# standard library
import re
from abc import ABC, abstractmethod
from urllib.parse import urlparse


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

    def __init__(self, host: str = None, port: int = None, scheme: str = None, uri: str = None):
        if uri:
            self.set_id(uri)
            if host and host != self.__host:
                raise Exception("Input host, port or scheme is different to the input uri ")
            if port is not None and port != self.__port:
                raise Exception("Input host, port or scheme is different to the input uri ")
            if scheme is not None and scheme != self.__scheme:
                raise Exception("Input host, port or scheme is different to the input uri ")
        elif host is None or scheme is None:
            raise Exception("Both host and scheme are required or You can give url only")
        else:
            self.__host = host
            self.__port = port
            self.__scheme = scheme

        self.__isAliveFlag = False
        self.__readyToServe = True
        self.__zone = self.UNKNOWN_ZONE

    @classmethod
    def combine_id(cls, host: str, port: int) -> str:
        return f"{host}:{port}"

    @classmethod
    def normalize_id(cls, uri: str) -> str:
        hostPort = cls.get_host_port(uri)

        if hostPort:
            return cls.combine_id(hostPort[0], hostPort[1])
        return None

    @classmethod
    def __get_scheme(cls, uri: str) -> str:
        if not uri:
            return None

        scheme = None
        uri = uri.lower()
        if uri.startswith("http://"):
            scheme = "http"
        elif uri.startswith("https://"):
            scheme = "https"

        return scheme

    @classmethod
    def get_host_port(cls, uri: str) -> tuple:
        if uri is None:
            return None

        uriPattern = r"https?:\/\/[^\/][^\/ :]*:\d+[\/]?.*"
        uri = uri.lower()
        port = 80

        if not re.fullmatch(uriPattern, uri):
            raise Exception("Not a valid uri!")

        result = urlparse(uri)
        host, port = re.split(":", result.netloc)
        port = int(port)

        cls.__host = host
        cls.__port = port
        cls.__scheme = result.scheme

        return (host, port)

    def set_host(self, host: str):
        if host is not None:
            self.__host = host
            self.__serverId = self.combine_id(host, self.__port)

    def set_port(self, port: int):
        self.__port = port
        if self.__host:
            self.__serverId = self.combine_id(self.__host, port)

    def set_zone(self, zone: str):
        self.__zone = zone

    def set_scheme(self, scheme: str):
        self.__scheme = scheme

    def set_id(self, uri: str):
        hostPort = self.get_host_port(uri)

        if hostPort is None:
            self.__serverId = None
        else:
            self.__serverId = self.combine_id(hostPort[0], hostPort[1])
            self.__host = hostPort[0]
            self.__port = hostPort[1]
            self.__scheme = self.__get_scheme(uri)

    def set_alive(self, isAliveFlag):
        self.__isAliveFlag = isAliveFlag

    def set_ready_to_serve(self, ready_to_serve: bool):
        self.__readyToServe = ready_to_serve

    def get_host(self) -> str:
        return self.__host

    def get_port(self) -> int:
        return self.__port

    def get_zone(self) -> str:
        return self.__zone

    def get_id(self) -> str:
        return self.__serverId

    def get_meta_info(self) -> MetaInfo:
        return self.__simple_meta_info

    def is_ready_to_serve(self) -> bool:
        return self.__readyToServe

    def is_alive(self) -> bool:
        return self.__isAliveFlag

    def __eq__(self, other):
        if type(self) == type(other):
            return self.__serverId == other.get_id()
        else:
            return False

    def __hash__(self):
        hashCode = 7
        serverId = self.get_id()
        hashCode = 31 * hashCode + (None == serverId and 0 or self.__hash__(serverId))

        return hashCode

    def __str__(self):
        return self.get_id()
