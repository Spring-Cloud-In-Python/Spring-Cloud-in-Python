# -*- coding: utf-8 -*-
# standard library
from abc import ABC, abstractmethod
from typing import Optional

# scip plugin
from commons.client.loadbalancer.factory import LoadBalancerClientFactory
from commons.client.service_instance import ServiceInstance
from commons.exceptions.primitive import raise_if_type_not_match

__author__ = "Waterball (johnny850807@gmail.com)"
__license__ = "Apache 2.0"


class ServiceInstanceChooser(ABC):
    @abstractmethod
    def choose(self, service_id: str, request=None) -> Optional[ServiceInstance]:
        """
        Choose an instance from the instances associated by the service_id,
        and it's expected that the choice is load-balanced.
        :param request: (opt) TODO not sure will we need this,
                                this extension was designed by spring-cloud.
        :param service_id: (str)
        :return: (ServiceInstance)
        """
        pass


class LoadBalancerClient(ServiceInstanceChooser, ABC):
    """
    The client which delegates to LoadBalancer SPIs.
    """

    @abstractmethod
    def execute(self):
        pass


class BlockingLoadBalancerClient(LoadBalancerClient):
    """
    The default implementation of LoadBalancerClient.
    """

    def __init__(self, loadbalancer_client_factory: LoadBalancerClientFactory):
        self.loadbalancer_client_factory = loadbalancer_client_factory

    def choose(self, service_id: str, request=None) -> Optional[ServiceInstance]:
        loadbalancer = self.loadbalancer_client_factory.get_instance(service_id)
        if not loadbalancer:
            return None
        raise_if_type_not_match(loadbalancer, LoadBalancer)
        return loadbalancer.choose(request=request)

    def execute(self):
        # TODO not sure if we really need this, this was designed by spring cloud
        pass


class LoadBalancer(ABC):
    """
    The LoadBalancer SPI interface.
    """

    @property
    @abstractmethod
    def service_id(self) -> str:
        pass

    @abstractmethod
    def choose(self, request=None) -> Optional[ServiceInstance]:
        """
        Make a load-balanced choice among several instances.
        :param request: (opt) TODO not sure will we need this,
                                this extension was designed by spring-cloud.
        :return: (ServiceInstance)
        """
        pass
