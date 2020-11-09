# -*- coding: utf-8 -*-
# standard library
from typing import List, Set

# scip plugin
from spring_cloud.commons.client import ServiceInstance

__author__ = "Waterball (johnny850807@gmail.com)"
__license__ = "Apache 2.0"

# scip plugin
from spring_cloud.commons.client.discovery.discovery_client import DiscoveryClient
from spring_cloud.commons.utils.functional_operators import flat_map
from spring_cloud.commons.utils.list_utils import not_none_nor_empty


class CompositeDiscoveryClient(DiscoveryClient):
    """
    Composite pattern application:
        aggregate the service sources from a list of discovery client
    """

    def __init__(self, *discovery_clients: DiscoveryClient):
        self.__discovery_clients = discovery_clients

    def get_instances(self, service_id: str) -> List[ServiceInstance]:
        for client in self.__discovery_clients:
            services = client.get_instances(service_id)
            if not_none_nor_empty(services):
                return services
        return []

    @property
    def services(self) -> Set[str]:
        return set(flat_map(lambda d: d.services, self.__discovery_clients))
