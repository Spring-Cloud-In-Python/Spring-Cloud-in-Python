# -*- coding: utf-8 -*-

# standard library
import ipaddress
import uuid
from abc import ABC, abstractmethod
from typing import Dict

# pypi/conda library
import netifaces

__author__ = "Haribo (haribo1558599@gmail.com)"
__license__ = "Apache 2.0"


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
    def is_instance_enabled_on_init(self) -> bool:
        raise NotImplemented

    @property
    @abstractmethod
    def unsecure_port(self) -> int:
        raise NotImplemented

    @property
    @abstractmethod
    def secure_port(self) -> int:
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


class DefaultEurekaInstanceConfig(EurekaInstanceConfig):
    def __init__(self, app_name: str = None):
        self._instance_id = str(uuid.uuid4())
        self._app_name = app_name
        self._host_name = next(self._get_local_non_loopback_ipv4_addresses())

    @staticmethod
    def _get_local_non_loopback_ipv4_addresses():
        for interface in netifaces.interfaces():
            # Not all interfaces have an IPv4 address:
            if netifaces.AF_INET in netifaces.ifaddresses(interface):
                # Some interfaces have multiple IPv4 addresses:
                for address_info in netifaces.ifaddresses(interface)[netifaces.AF_INET]:
                    address_object = ipaddress.IPv4Address(address_info["addr"])
                    if not address_object.is_loopback:
                        yield address_info["addr"]

    @property
    def instance_id(self) -> str:
        return self._instance_id

    @property
    def app_name(self) -> str:
        return self._app_name

    @app_name.setter
    def app_name(self, app_name: str):
        self._app_name = app_name

    @property
    def is_instance_enabled_on_init(self) -> bool:
        return False

    @property
    def unsecure_port(self) -> int:
        return 80

    @property
    def secure_port(self) -> int:
        return 443

    @property
    def is_unsecure_port_enabled(self) -> bool:
        return True

    @property
    def is_secure_port_enabled(self) -> bool:
        return False

    @property
    def lease_renewal_interval_in_secs(self) -> int:
        return 30

    @property
    def lease_expiration_duration_in_secs(self) -> int:
        return 90

    @property
    def virtual_host_name(self) -> str:
        return self.host_name + ":" + str(self.unsecure_port)

    @property
    def secure_virtual_host_name(self) -> str:
        return self.host_name + ":" + str(self.secure_port)

    @property
    def host_name(self) -> str:
        return self._host_name

    @host_name.setter
    def host_name(self, host_name: str):
        self._host_name = host_name

    @property
    def metadata(self) -> Dict[str, str]:
        return {}

    @property
    def ip_address(self) -> str:
        return "127.0.0.1"
