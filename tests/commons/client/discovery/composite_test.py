# -*- coding: utf-8 -*-

__author__ = "Waterball (johnny850807@gmail.com)"
__license__ = "Apache 2.0"

# scip plugin
from spring_cloud.commons.client.discovery import CompositeDiscoveryClient, static_discovery_client

client = CompositeDiscoveryClient(
    static_discovery_client("url-1", "service-1", ["1-1", "1-2", "1-3"]),
    static_discovery_client("url-2", "service-2", ["2-1", "2-2", "2-3"]),
    static_discovery_client("url-3", "service-3", ["3-1", "3-2", "3-3"]),
)


def test_get_instances():
    for service_id in range(1, 4):
        instances = client.get_instances(f"service-{service_id}")
        for instance_id in range(1, 4):
            instance = instances[instance_id - 1]
            assert f"{service_id}-{instance_id}" == instance.instance_id


def test_get_services():
    services = client.services
    assert {"service-1", "service-2", "service-3"} == services
