# -*- coding: utf-8 -*-

# standard library
from abc import ABC, abstractmethod

__author__ = "Haribo (haribo1558599@gmail.com)"
__license__ = "Apache 2.0"

# standard library
from typing import Dict


class EurekaInstanceConfig(ABC):
    """
    Configuration information required by the instance to register with Eureka
    server. Once registered, users can look up information from
    EurekaClient based on virtual hostname (also called VIPAddress),
    the most common way of doing it or by other means to get the information
    necessary to talk to other instances registered with Eureka server.

    See com.netflix.appinfo.EurekaInstanceConfig.
    """

    @property
    @abstractmethod
    def instance_id(self) -> str:
        raise NotImplemented

    @property
    @abstractmethod
    def app_name(self) -> str:
        raise NotImplemented

    @property
    @abstractmethod
    def app_group_name(self) -> str:
        raise NotImplemented

    @property
    @abstractmethod
    def is_instance_enabled_on_init(self) -> bool:
        raise NotImplemented

    @property
    @abstractmethod
    def unsecure_port(self) -> int:
        raise NotImplemented

    @property
    @abstractmethod
    def secure_port(self) -> str:
        raise NotImplemented

    @property
    @abstractmethod
    def is_unsecure_port_enabled(self) -> bool:
        raise NotImplemented

    @property
    @abstractmethod
    def is_secure_port_enabled(self) -> bool:
        raise NotImplemented

    @property
    @abstractmethod
    def lease_renewal_interval_in_secs(self) -> int:
        raise NotImplemented

    @property
    @abstractmethod
    def lease_expiration_duration_in_secs(self) -> int:
        raise NotImplemented

    @property
    @abstractmethod
    def virtual_host_name(self) -> str:
        raise NotImplemented

    @property
    @abstractmethod
    def secure_virtual_host_name(self) -> str:
        raise NotImplemented

    @property
    @abstractmethod
    def host_name(self) -> str:
        raise NotImplemented

    @property
    @abstractmethod
    def metadata(self) -> Dict[str, str]:
        raise NotImplemented

    @property
    @abstractmethod
    def ip_address(self) -> str:
        raise NotImplemented

    @property
    @abstractmethod
    def status_page_url(self) -> str:
        raise NotImplemented

    @property
    @abstractmethod
    def home_page_url(self) -> str:
        raise NotImplemented

    @property
    @abstractmethod
    def health_check_page_url(self) -> str:
        raise NotImplemented

    @property
    @abstractmethod
    def secure_health_check_page_url(self) -> str:
        raise NotImplemented
