# scip plugin
from commons.client.discovery.discovery_client import DiscoveryClient
from commons.utils.functional_operators import flat_map
from commons.utils.list_utils import not_null_nor_empty

__author__ = "Waterball (johnny850807@gmail.com)"
__license__ = "Apache 2.0"


class CompositeDiscoveryClient(DiscoveryClient):
    def __init__(self, *discovery_clients):
        self.discovery_clients = discovery_clients

    def get_instances(self, service_id):
        for client in self.discovery_clients:
            services = client.get_instances(service_id)
            if not_null_nor_empty(services):
                return services
        return []

    @property
    def services(self):
        return flat_map(lambda d: d.services, self.discovery_clients)
