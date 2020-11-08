# -*- coding: utf-8 -*-
# standard library
from abc import ABC, abstractmethod
from typing import List

# scip plugin
from commons.client.loadbalancer.round_robin import RoundRobinLoadBalancer
from commons.client.loadbalancer.supplier.service_instance_list_supplier import FixedServiceInstanceListSupplier
from commons.client.service_instance import ServiceInstance
from external.cache.cache_manager import NaiveCacheManager

__author__ = "Waterball (johnny850807@gmail.com)"
__license__ = "Apache 2.0"


class LoadBalancerClientFactory(ABC):
    """
    An abstract factory which creates a family of instances associated with a service_id
    """

    @staticmethod
    def default(instances: List[ServiceInstance]):
        return DefaultLoadBalancerClientFactory(instances)

    @abstractmethod
    def get_loadbalancer(self, service_id: str):
        """
        :return: (LoadBalancer)
        """
        pass

    @abstractmethod
    def get_service_instance_list_supplier(self, service_id: str):
        """
        :return: (ServiceInstanceListSupplier)
        """
        pass


class DefaultLoadBalancerClientFactory(LoadBalancerClientFactory):
    def __init__(self, instances: List[ServiceInstance]):
        self.loadbalancers = NaiveCacheManager()  # service_id --> LoadBalancer
        self.instances_suppliers = NaiveCacheManager()  # service_id --> ServiceInstanceListSupplier
        self.__instances = instances

    def get_loadbalancer(self, service_id: str):
        return self.loadbalancers.get(service_id).on_cache_miss(
            lambda: RoundRobinLoadBalancer(self.get_service_instance_list_supplier(service_id), service_id)
        )

    def get_service_instance_list_supplier(self, service_id: str):
        return self.instances_suppliers.get(service_id).on_cache_miss(
            lambda: FixedServiceInstanceListSupplier(service_id, self.__instances)
        )
