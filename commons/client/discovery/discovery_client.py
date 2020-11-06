# -*- coding: utf-8 -*-
"""
DiscoveryClient is responsible for providing a list of service's instances.
There may be many services, for example: 'user-service', 'order-service', 'product-service', and so on.
Where each service may have several instances registered (e.g. user-service-1, user-service-2, ...),
and the registered instances are called ServiceInstances.
"""

# standard library
from abc import ABC, abstractmethod

# scip plugin
from commons.client.ServiceInstance import StaticServiceInstance
from commons.utils.functional_operators import filter_get_first

__author__ = "Waterball (johnny850807@gmail.com)"
__license__ = "Apache 2.0"


class DiscoveryClient(ABC):
    @abstractmethod
    def get_instances(self, service_id):
        """
        Gets all ServiceInstances associated with a particular serviceId.
        :param service_id: (str) The serviceId to query.
        :return: A List of ServiceInstance.
        """
        pass

    @property
    @abstractmethod
    def services(self):
        """
        :return: All known service IDs (*str).
        """
        pass


class StaticDiscoveryClient(DiscoveryClient):
    """
    A DiscoveryClient initialized with the services.
    """

    def __init__(self, services):
        self.__services = services

    def get_instances(self, service_id):
        return list(filter(lambda s: s.service_id == service_id, self.services))

    @property
    def services(self):
        return self.__services


def static_discovery_client(uri, service_id, instance_ids):
    """
    A helper method that helps create a list of instances from the same service.
    :param uri the uri of every service's
    :param service_id the service_id of the service
    :param instance_ids a list of ids (*str) of the instances'
    Usage:
        static_discovery_client("url-1", "service-1", ["id-1", "id-2", "id-3"])
    """
    services = [StaticServiceInstance(uri, service_id, instance_id) for instance_id in instance_ids]
    return StaticDiscoveryClient(services)
