# -*- coding: utf-8 -*-

__author__ = "Waterball (johnny850807@gmail.com)"
__license__ = "Apache 2.0"

# scip plugin
from commons.client.discovery.discovery_client import DiscoveryClient
from commons.utils.functional_operators import flat_map
from commons.utils.list_utils import not_none_nor_empty


class CompositeDiscoveryClient(DiscoveryClient):
    """
    Composite pattern application:
        aggregate the service sources from a list of discovery client
    """

    def __init__(self, *discovery_clients):
        """
        :param discovery_clients: a list of DiscoveryClient
        """
        self.__discovery_clients = discovery_clients

    def get_instances(self, service_id):
        for client in self.__discovery_clients:
            services = client.get_instances(service_id)
            if not_none_nor_empty(services):
                return services
        return []

    @property
    def services(self):
        return flat_map(lambda d: d.services, self.__discovery_clients)
