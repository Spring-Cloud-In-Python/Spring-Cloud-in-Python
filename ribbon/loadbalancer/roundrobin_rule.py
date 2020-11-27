# -*- coding: utf-8 -*-

__author__ = "MJ (tsngmj@gmail.com)"
__license__ = "Apache 2.0"

# standard library
import time
import warnings

# scip plugin
from ribbon.loadbalancer.abstract_loadbalance_rule import AbstractLoadBalanceRule
from ribbon.loadbalancer.loadbalancer import LoadBalancer
from ribbon.loadbalancer.server import Server
from spring_cloud.utils.atomic import AtomicInteger


class RoundRobinRule(AbstractLoadBalanceRule):
    __AVAILABLE_ONLY_SERVERS = True
    __ALL_SERVERS = False

    def __init__(self, lb: LoadBalancer = None):
        self.__lb = lb
        self.__nextServerCyclicCounter = AtomicInteger()

    def choose(self, lb: LoadBalancer = None) -> Server:
        if lb is None and self.__lb is None:
            self.log("no load balancer")
            return None

        elif lb is None:
            lb = self.__lb

        server: Server = None
        count = 0

        while server is None and count < 10:
            count += 1

            reachableServers: list[Server] = lb.get_reachable_servers()
            allServers: list[Server] = lb.get_all_servers()

            upCount = len(reachableServers)
            serverCount = len(allServers)

            if upCount == 0 or serverCount == 0:
                self.log("No up servers available from load balancer: " + lb)
                return None

            nextServerIndex = self.__increment_and_get_modulo(serverCount)

            server = allServers[nextServerIndex]

            if server is None:
                """
                time.sleep(0) can make it like thread.yield in java
                """
                time.sleep(0)
                continue

            if server.is_alive() and server.is_ready_to_serve():
                return server

            else:
                server = None

        if count > 10:
            self.log("No available alive servers after 10 tries from load balancer: " + lb)

        return server

    def __increment_and_get_modulo(self, modulo: int) -> int:
        """
        :param modulo: The modulo to bound the value of the counter.
        :return: The next int value.
        """
        while True:
            currIndex = self.__nextServerCyclicCounter.get()
            nextIndex = (currIndex + 1) % modulo
            if self.__nextServerCyclicCounter.compare_and_set(currIndex, nextIndex):
                return nextIndex

    def log(self, msg: str):
        warnings.warn(msg, RuntimeWarning)
