# -*- coding: utf-8 -*-
"""
Since the load-balancer is responsible for choosing one instance
per service request from a list of instances. We need a ServiceInstanceListSupplier for
each service to decouple the source of the instances from load-balancers.
"""
# standard library
from abc import ABC, abstractmethod

# scip plugin
from commons.client.discovery.discovery_client import DiscoveryClient

__author__ = "Waterball (johnny850807@gmail.com)"
__license__ = "Apache 2.0"


class ServiceInstanceListSupplier(ABC):
    """
    Non-Reactive version of ServiceInstanceListSupplier.
    (Spring Cloud implement the supplier in the reactive way, means that
    its supplier returns an Observable which broadcasts the instances on every change.)

    We may consider to adopt reactive programming in the future.
    """

    @property
    @abstractmethod
    def service_id(self):
        """
        :return: (str) the service's id
        """
        pass

    @abstractmethod
    def get(self, request=None):
        """
        :param request (opt) TODO not sure will we need this,
                        this extension was designed by spring-cloud.
        :return: (*ServiceInstance) a list of instances
        """
        pass


class FixedServiceInstanceListSupplier(ServiceInstanceListSupplier):
    """
    A supplier that is initialized with fixed instances. (i.e. they won't be changed)
    """

    def __init__(self, service_id, instances):
        """
        :param service_id: (str)
        :param instances: (*ServiceInstance)
        """
        self._service_id = service_id
        self._instances = instances

    def get(self, request=None):
        return self._instances

    @property
    def service_id(self):
        return self._service_id


class DiscoveryClientServiceInstanceListSupplier(ServiceInstanceListSupplier):
    """
    The adapter delegating to discovery client for querying instances
    """

    def __init__(self, service_id, discovery_client):
        """
        :param service_id: (str)
        :param discovery_client: (DiscoveryClient)
        """
        self.__service_id = service_id
        self.__delegate = discovery_client

    @property
    def service_id(self):
        return self.__service_id

    def get(self, request=None):
        return self.__delegate.get_instances()
