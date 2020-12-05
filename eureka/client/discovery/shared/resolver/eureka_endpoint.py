# standard library
from abc import ABC, abstractmethod
from urllib.parse import urlparse

__author__ = "Haribo (haribo1558599@gmail.com)"
__license__ = "Apache 2.0"


class EurekaEndpoint(ABC):
    @property
    @abstractmethod
    def service_url(self) -> str:
        raise NotImplemented

    @property
    @abstractmethod
    def host_name(self) -> str:
        raise NotImplemented

    @property
    @abstractmethod
    def relative_uri(self) -> str:
        raise NotImplemented

    @property
    @abstractmethod
    def port(self) -> int:
        raise NotImplemented

    @property
    @abstractmethod
    def is_secure(self) -> bool:
        raise NotImplemented


class DefaultEndpoint(EurekaEndpoint):
    __slots__ = (
        "_service_url",
        "_parsed_url",
    )

    def __init__(self, service_url: str):
        self._service_url = service_url
        self._parsed_url = None

        try:
            self._parsed_url = urlparse(self._service_url)
        except Exception:
            raise ValueError("Malformed service_url: " + self._service_url)

    @property
    def service_url(self) -> str:
        return self._service_url

    @property
    def host_name(self) -> str:
        return self._parsed_url.hostname

    @property
    def relative_uri(self) -> str:
        return self._parsed_url.path

    @property
    def port(self) -> int:
        return self._parsed_url.port

    @property
    def is_secure(self) -> bool:
        return self._parsed_url.scheme == "https"
