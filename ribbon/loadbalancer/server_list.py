# -*- coding: utf-8 -*-

__author__ = "MJ (tsngmj@gmail.com)"
__license__ = "Apache 2.0"

# standard library
from abc import ABC, abstractmethod

"""
Interface that defines the methods sed to obtain the List of Servers
"""

# scip plugin
from ribbon.loadbalancer.server import Server


class ServerList(ABC):
    @abstractmethod
    def get_initial_list_of_servers(self) -> Server:
        pass

    @abstractmethod
    def get_updated_list_of_servers(self) -> Server:
        pass
