# -*- coding: utf-8 -*-

# standard library
from abc import ABC, abstractmethod
from typing import List, TypeVar

# scip plugin
from eureka.client.app_info.instance_info import InstanceInfo
from eureka.client.discovery.eureka_client_config import EurekaClientConfig
from eureka.client.discovery.shared.application import Application
from eureka.client.discovery.shared.applications import Applications

__author__ = "Haribo (haribo1558599@gmail.com)"
__license__ = "Apache 2.0"

ApplicationInfoManager = TypeVar("ApplicationInfoManager")


class EurekaClient(ABC):
    """
    Define a simple interface over the current DiscoveryClient implementation.

    EurekaClient API contracts are:
        - provide the ability to get InstanceInfo(s) (in various different ways)
        - provide the ability to get data about the local client

    See com.netflix.discovery.EurekaClient.
    """

    @abstractmethod
    def get_application(self, application_name: str) -> Application:
        raise NotImplemented

    @abstractmethod
    def get_applications(self) -> Applications:
        raise NotImplemented

    @abstractmethod
    def get_next_instance_from_eureka_server(self, virtual_host_name: str, secure: bool) -> InstanceInfo:
        raise NotImplemented

    @abstractmethod
    def get_instances_by_virtual_host_name(self, virtual_host_name: str, secure: bool) -> List[InstanceInfo]:
        raise NotImplemented

    @property
    @abstractmethod
    def eureka_client_config(self) -> EurekaClientConfig:
        raise NotImplemented

    @property
    @abstractmethod
    def application_info_manager(self) -> ApplicationInfoManager:
        raise NotImplemented

    @abstractmethod
    def shutdown(self):
        pass
