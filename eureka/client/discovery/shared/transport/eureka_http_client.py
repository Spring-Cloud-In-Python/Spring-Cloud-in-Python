# standard library
from abc import ABC, abstractmethod

__author__ = "Haribo (haribo1558599@gmail.com)"
__license__ = "Apache 2.0"

# standard library
from typing import Union

# scip plugin
from eureka.client.app_info.instance_info import InstanceInfo
from eureka.client.discovery.shared.transport.eureka_http_response import EurekaHttpResponse


class EurekaHttpClient(ABC):
    @abstractmethod
    def register(self, instance: InstanceInfo) -> Union[EurekaHttpResponse, None]:
        raise NotImplemented

    @abstractmethod
    def cancel(self, instance: InstanceInfo) -> Union[EurekaHttpResponse, None]:
        raise NotImplemented

    @abstractmethod
    def get_applications(self) -> Union[EurekaHttpResponse, None]:
        raise NotImplemented

    @abstractmethod
    def shutdown(self):
        raise NotImplemented
