# -*- coding: utf-8 -*-
# scip plugin
from spring_cloud.commons.client.loadbalancer import LoadBalancerClientFactory
from tests.commons.client.loadbalancer.stubs import INSTANCES

__author__ = "Waterball (johnny850807@gmail.com)"
__license__ = "Apache 2.0"

factory = LoadBalancerClientFactory.default(INSTANCES)


class TestLoadBalancerClientFactory:
    def test_should_create_instances_associated_with_service_id(self):
        loadbalancer = factory.get_loadbalancer("1")
        assert loadbalancer.service_id == "1"
        instances_supplier = factory.get_service_instance_list_supplier("2")
        assert instances_supplier.service_id == "2"

    def test_should_create_singleton_instances(self):
        assert factory.get_loadbalancer("1") == factory.get_loadbalancer("1")
        assert factory.get_service_instance_list_supplier("1") == factory.get_service_instance_list_supplier("1")
