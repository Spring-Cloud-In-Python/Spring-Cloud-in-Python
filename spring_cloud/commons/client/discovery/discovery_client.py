# -*- coding: utf-8 -*-
"""
DiscoveryClient is responsible for providing a list of service's instances.
There may be many services, for example: 'user-service', 'order-service', 'product-service', and so on.
Where each service may have several instances registered (e.g. user-service-1, user-service-2, ...),
and the registered instances are called ServiceInstances.
"""

# standard library
from abc import ABC, abstractmethod
from typing import List, Set

# scip plugin
from spring_cloud.commons.client import ServiceInstance, StaticServiceInstance

__author__ = "Waterball (johnny850807@gmail.com)"
__license__ = "Apache 2.0"


class DiscoveryClient(ABC):
    @abstractmethod
    def get_instances(self, service_id: str) -> List[ServiceInstance]:
        """
        Gets all ServiceInstances associated with a particular serviceId.
        :param service_id: (str) The serviceId to query.
        :return: A List of ServiceInstance.
        """
        pass

    @property
    @abstractmethod
    def services(self) -> List[str]:
        """
        :return: All known service IDs (*str).
        """
        pass


class StaticDiscoveryClient(DiscoveryClient):
    """
    A DiscoveryClient initialized with the services.
    """

    def __init__(self, instances: List[ServiceInstance]):
        self.__instances = instances

    def get_instances(self, service_id: str) -> List[ServiceInstance]:
        return list(filter(lambda s: s.service_id == service_id, self.__instances))

    @property
    def services(self) -> Set[str]:
        return {s.service_id for s in self.__instances}


def static_discovery_client(uri: str, service_id: str, instance_ids: List[str]) -> StaticDiscoveryClient:
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
