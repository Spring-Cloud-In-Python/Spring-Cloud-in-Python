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
            self.id = uri
            if host and host != self.__host:
                raise Exception("Input host, port or scheme is different to the input uri ")
            if port is not None and port != self.__port:
                raise Exception("Input host, port or scheme is different to the input uri ")
            if scheme is not None and scheme != self.__scheme:
                raise Exception("Input host, port or scheme is different to the input uri ")
        elif host is None or port is None:
            raise Exception("Both host and port are required or You can give url only")
        else:
            self.__host = host
            self.__port = port or 80
            self.__id = self.combine_id(host, port)
            self.__scheme = scheme

        self.__is_alive = False
        self.__is_ready_to_serve = True
        self.__zone = self.UNKNOWN_ZONE

    @classmethod
    def combine_id(cls, host: str, port: int) -> str:
        return f"{host}:{port}"

    @classmethod
    def normalize_id(cls, uri: str) -> str:
        host_port = cls.get_host_port(uri)

        if host_port:
            return cls.combine_id(host_port[0], host_port[1])
        return None

    @classmethod
    def get_host_port(cls, uri: str) -> tuple:
        if uri is None:
            return None

        uri_pattern = r"https?:\/\/[^\/][^\/ :]*:\d+[\/]?.*"
        uri = uri.lower()
        port = 80

        if not re.fullmatch(uri_pattern, uri):
            raise Exception("Not a valid uri!")

        result = urlparse(uri)
        host, port = re.split(":", result.netloc)
        port = int(port)

        cls.__host = host
        cls.__port = port
        cls.__scheme = result.scheme

        return (host, port)

    @property
    def host(self) -> str:
        return self.__host

    @host.setter
    def host(self, host: str):
        if host is not None:
            self.__host = host
            self.__id = self.combine_id(host, self.__port)

    @property
    def port(self) -> int:
        return self.__port

    @port.setter
    def port(self, port: int):
        self.__port = port
        if self.__host:
            self.__id = self.combine_id(self.__host, port)

    @property
    def zone(self) -> str:
        return self.__zone

    @zone.setter
    def zone(self, zone: str):
        self.__zone = zone

    @property
    def scheme(self, uri: str) -> str:
        if not uri:
            return None

        scheme = None
        uri = uri.lower()
        if uri.startswith("http://"):
            scheme = "http"
        elif uri.startswith("https://"):
            scheme = "https"

        return scheme

    @scheme.setter
    def scheme(self, scheme: str):
        self.__scheme = scheme

    @property
    def id(self) -> str:
        return self.__id

    @id.setter
    def id(self, uri: str):
        host_port = self.get_host_port(uri)

        if host_port is None:
            self.__id = None
        else:
            self.__id = self.combine_id(host_port[0], host_port[1])
            self.__host = host_port[0]
            self.__port = host_port[1]

    @property
    def is_alive(self) -> bool:
        return self.__is_alive

    @is_alive.setter
    def is_alive(self, is_alive):
        self.__is_alive = is_alive

    @property
    def is_ready_to_serve(self) -> bool:
        return self.__is_ready_to_serve

    @is_ready_to_serve.setter
    def is_ready_to_serve(self, is_ready_to_serve: bool):
        self.__is_ready_to_serve = is_ready_to_serve

    @property
    def meta_info(self) -> MetaInfo:
        return self.__simple_meta_info

    def __eq__(self, other):
        if type(self) == type(other):
            return self.__id == other.get_id()
        else:
            return False

    def __hash__(self):
        hash_code = 7
        server_id = self.get_id()
        hash_code = 31 * hash_code + (None == server_id and 0 or self.__hash__(server_id))

        return hash_code

    def __str__(self):
        return self.get_id()
