# standard library
from abc import ABC, abstractmethod
from typing import List

__author__ = "Haribo (haribo1558599@gmail.com)"
__license__ = "Apache 2.0"

# scip plugin
from eureka.client.discovery.eureka_client_config import EurekaClientConfig
from eureka.client.discovery.shared.resolver.eureka_endpoint import DefaultEndpoint, EurekaEndpoint


class ClusterResolver(ABC):
    @abstractmethod
    def get_cluster_endpoints(self) -> List[EurekaEndpoint]:
        raise NotImplemented


class DefaultClusterResolver(ClusterResolver):
    def __init__(self, eureka_client_config: EurekaClientConfig):
        self._eureka_client_config = eureka_client_config

    def get_cluster_endpoints(self) -> List[EurekaEndpoint]:
        eureka_server_service_urls = self._eureka_client_config.eureka_server_service_urls

        return [DefaultEndpoint(service_url) for service_url in eureka_server_service_urls]
