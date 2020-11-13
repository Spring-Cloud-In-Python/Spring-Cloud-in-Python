# -*- coding: utf-8 -*-
# standard library
from unittest.mock import Mock

# scip plugin
from spring_cloud.commons.client.loadbalancer.supplier import (
    DiscoveryClientServiceInstanceListSupplier,
    FixedServiceInstanceListSupplier,
)
from tests.commons.client.loadbalancer.stubs import INSTANCES, SERVICE_ID

__author__ = "Waterball (johnny850807@gmail.com)"
__license__ = "Apache 2.0"


class TestFixedServiceInstanceListSupplier:
    def setup_class(self):
        self.supplier = FixedServiceInstanceListSupplier(SERVICE_ID, INSTANCES)

    def test_get_service_id(self):
        assert SERVICE_ID == self.supplier.service_id

    def test_get_instances(self):
        assert INSTANCES == self.supplier.get()


class TestDiscoveryClientServiceInstanceListSupplier:
    def setup_class(self):
        self.discovery_client = Mock()
        self.discovery_client.get_instances = Mock(return_value=INSTANCES)
        self.supplier = DiscoveryClientServiceInstanceListSupplier(SERVICE_ID, self.discovery_client)

    def test_get_service_id(self):
        assert SERVICE_ID == self.supplier.service_id

    def test_get_instances(self):
        assert INSTANCES == self.supplier.get()
