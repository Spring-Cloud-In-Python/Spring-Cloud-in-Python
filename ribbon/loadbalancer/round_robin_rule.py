# -*- coding: utf-8 -*-
# scip plugin
from spring_cloud.utils import logging

__author__ = "MJ (tsngmj@gmail.com)"
__license__ = "Apache 2.0"

# standard library
import time
import warnings
from typing import List

# scip plugin
from ribbon.loadbalancer.load_balance_rule import LoadBalanceRule
from ribbon.loadbalancer.load_balancer import LoadBalancer
from ribbon.loadbalancer.server import Server
from spring_cloud.utils.atomic import AtomicInteger
from spring_cloud.utils.logging import getLogger


class RoundRobinRule(LoadBalanceRule):
    __AVAILABLE_ONLY_SERVERS = True
    __ALL_SERVERS = False

    def __init__(self, lb: LoadBalancer = None):
        self.logger = logging.getLogger(f"ribbon.RoundRobinRule")
        self.__lb = lb
        self.__nextServerCyclicCounter = AtomicInteger()

    def choose(self, lb: LoadBalancer = None, key: object = None) -> Server:
        lb = lb or self.__lb

        server: Server = None
        count = 0

        if lb:
            self.logger.trace(f"({lb.name}) RR is being performed (pos={self.__nextServerCyclicCounter})...")
            while not server and count < 10:
                count += 1

                reachableServers: List[Server] = lb.get_reachable_servers()
                allServers: List[Server] = lb.get_all_servers()

                upCount = len(reachableServers)
                serverCount = len(allServers)

                if upCount == 0 or serverCount == 0:
                    self.logger.warning(f"No up servers available from load balancer: {lb}")
                    return None

                nextServerIndex = self.__increment_and_get_modulo(serverCount)
                server = allServers[nextServerIndex]

                if server is None:
                    time.sleep(0)
                    continue

                if server.is_alive and server.is_ready_to_serve:
                    self.logger.trace(f"RoundRobin algorithm is completed. (pos={self.__nextServerCyclicCounter}).")
                    return server

                else:
                    server = None

            if count > 10:
                self.logger.warning(f"No available alive servers after 10 tries from load balancer: {lb}")

        self.logger.warning("no load balancer")

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

    @property
    def loadbalancer(self):
        return self.__lb

    @loadbalancer.setter
    def loadbalancer(self, lb: LoadBalancer):
        self.__lb = lb

    def __str__(self):
        return "RoundRobinRule"
