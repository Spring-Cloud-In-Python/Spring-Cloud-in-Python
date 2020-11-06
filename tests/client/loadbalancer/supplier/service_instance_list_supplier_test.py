# -*- coding: utf-8 -*-
# scip plugin
from commons.client.loadbalancer.supplier.service_instance_list_supplier import FixedServiceInstanceListSupplier
from commons.client.service_instance import StaticServiceInstance

__author__ = "Waterball (johnny850807@gmail.com)"
__license__ = "Apache 2.0"

SERVICE_ID = "serviceId"
instances = [StaticServiceInstance("uri", SERVICE_ID, instance_id) for instance_id in ["1", "2", "3"]]
supplier = FixedServiceInstanceListSupplier(SERVICE_ID, instances)


def test_get_service_id():
    assert SERVICE_ID == supplier.service_id


def test_get_instances():
    assert instances == supplier.get()
