# standard library
from abc import ABC, abstractmethod
from urllib.parse import urlparse

__author__ = "Waterball (johnny850807@gmail.com)"
__license__ = "Apache 2.0"


class ServiceInstance(ABC):
    @property
    @abstractmethod
    def instance_id(self):
        pass

    @property
    @abstractmethod
    def service_id(self):
        pass

    @property
    @abstractmethod
    def host(self):
        pass

    @property
    @abstractmethod
    def port(self):
        pass

    @property
    @abstractmethod
    def secure(self):
        pass

    @property
    @abstractmethod
    def uri(self):
        pass

    @property
    @abstractmethod
    def scheme(self):
        pass


class StaticServiceInstance(ServiceInstance):
    """
    A service instance that is initialized with its basic properties
    """

    def __init__(self, uri, service_id, instance_id):
        """
        :param uri: the url in the string type
        """
        url_obj = urlparse(uri)
        self._uri = uri
        self._scheme = url_obj.scheme
        self._secure = self._scheme == "https"
        self._host = url_obj.netloc
        self._port = url_obj.port
        self._service_id = service_id
        self._instance_id = instance_id

    @property
    def service_id(self):
        return self._service_id

    @property
    def instance_id(self):
        return self._instance_id

    @property
    def host(self):
        return self._host

    @property
    def port(self):
        return self._port

    @property
    def secure(self):
        return self._secure

    @property
    def uri(self):
        return self._uri

    @property
    def scheme(self):
        return self._scheme
