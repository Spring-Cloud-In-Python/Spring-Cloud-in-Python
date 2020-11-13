# -*- coding: utf-8 -*-

# standard library
from abc import ABC, abstractmethod
from typing import Union

# scip plugin
from spring_cloud.commons.client import ServiceInstance

__author__ = "Waterball (johnny850807@gmail.com)"
__license__ = "Apache 2.0"


class LoadBalancer(ABC):
    """
    The LoadBalancer SPI interface.
    """

    @property
    @abstractmethod
    def service_id(self) -> str:
        pass

    @abstractmethod
    def choose(self, request=None) -> Union[ServiceInstance, None]:
        """
        Make a load-balanced choice among several instances.
        :param request: (opt) TODO not sure will we need this,
                                this extension was designed by spring-cloud.
        :return: (ServiceInstance)
        """
        pass
