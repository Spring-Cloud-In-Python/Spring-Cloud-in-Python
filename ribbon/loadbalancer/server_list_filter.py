# -*- coding: utf-8 -*-

__author__ = "MJ (tsngmj@gmail.com)"
__license__ = "Apache 2.0"

# standard library
from abc import ABC, abstractmethod
from typing import List

# scip plugin
from ribbon.loadbalancer.server import Server


class ServerListFilter(ABC):
    @abstractmethod
    def get_filtered_list_of_servers(self, servers: List[Server]) -> List[Server]:
        pass
