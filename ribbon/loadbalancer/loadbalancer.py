# -*- coding: utf-8 -*-

__author__ = "MJ (tsngmj@gmail.com)"
__license__ = "Apache 2.0"

# standard library
from abc import ABC, abstractmethod
from typing import List

# scip plugin
from ribbon.loadbalancer.server import Server

"""
Interface that defines the operations for a software loadbalancer.
A typical loadbalancer minimally need a set of servers to loadbalance for,
a method to mark a particular server to be out of rotation and a call that will
choose a server from the existing list of server.
"""


class LoadBalancer(ABC):
    @abstractmethod
    def addServers(self, servers: List[Server]):
        """
        Initial list of servers. This API also serves to add additional ones at a later time.
        :param newServers: A list of Servers
        """
        pass

    @abstractmethod
    def chooseServer(self, key: object) -> Server:
        """
        Choose a server from load balancer.
        :param key: An object that the load balancer may use to determine which server to return.
                    null if the load balancer does not use this parameter.
        :return: A chosen Server
        """
        pass

    @abstractmethod
    def markServerDown(self, server: Server):
        """
        To be called by the clients of the load balancer to notify that if a Server is down
        else, the LB will think its still Alive until the next Ping cycle - potentially
        :param server: Server to mark down
        """
        pass

    @abstractmethod
    def getReachableServers(self) -> List[Server]:
        """
        Only return the servers that are up and reachable.
        :return: A List of Servers
        """
        pass

    def getAllServers(self):
        """
        Return all known servers, both reachable and unreachable.
        :return: A List of Servers
        """
        pass
