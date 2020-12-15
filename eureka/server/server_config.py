# -*- coding: utf-8 -*-

__author__ = "Daniel1147 (sxn91401@gmail.com)"
__license__ = "Apache 2.0"

# standard library
from abc import ABC, abstractmethod


class ServerConfig(ABC):
    """

    The configuration for starting up the eureka server. It allows clients to override the entities through setters.

    """

    @property
    @abstractmethod
    def host(self) -> str:
        pass

    @host.setter
    @abstractmethod
    def host(self, value: str) -> None:
        pass

    @property
    @abstractmethod
    def port(self) -> int:
        pass

    @port.setter
    @abstractmethod
    def port(self, value: int) -> None:
        pass


class DefaultServerConfig(ServerConfig):
    def __init__(self):
        self.__host = "0.0.0.0"
        self.port = 8000

    @property
    def host(self) -> str:
        return self.__host

    @host.setter
    def host(self, value: str) -> None:
        self.__host = value

    @property
    def port(self) -> int:
        return self.__port

    @port.setter
    def port(self, value: int) -> None:
        self.__port = value
