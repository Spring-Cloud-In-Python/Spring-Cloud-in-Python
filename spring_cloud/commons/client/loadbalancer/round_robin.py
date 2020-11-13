# -*- coding: utf-8 -*-
"""
The built-in Round-Robin algorithm.
"""

# standard library
from typing import Union

# scip plugin
from spring_cloud.commons.client.service_instance import ServiceInstance
from spring_cloud.commons.utils.atomic import AtomicInteger

from .loadbalancer import LoadBalancer
from .supplier import ServiceInstanceListSupplier

__author__ = "Waterball (johnny850807@gmail.com)"
__license__ = "Apache 2.0"


class RoundRobinLoadBalancer(LoadBalancer):
    """
    A very easy thread-safe implementation adopting round-robin (RR) algorithm.
    """

    def __init__(self, instances_supplier: ServiceInstanceListSupplier, service_id):
        assert instances_supplier.service_id == service_id, "Inconsistent service's id."
        self.__instances_supplier = instances_supplier
        self.__service_id = service_id
        self.__position = AtomicInteger(-1)

    @property
    def service_id(self) -> str:
        return self.__service_id

    def choose(self, request=None) -> Union[ServiceInstance, None]:
        instances = self.__instances_supplier.get(request=request)
        pos = abs(self.__position.increment_and_get())
        return instances[pos % len(instances)]
