# -*- coding: utf-8 -*-

__author__ = "Ricky"
__license__ = "Apache 2.0"

# standard library
from typing import List

# scip plugin
from spring_cloud.commons.client.discovery.discovery_client import DiscoveryClient
from spring_cloud.commons.client.service_instance import ServiceInstance
from spring_cloud.eureka.eureka_service_instance import EurekaServiceInstance


class EurekaDiscoveryClient(DiscoveryClient):
    def __init__(self, eureka_client, client_config):
        self.DESCRIPTION = "Spring Cloud Eureka Discovery Client"
        self.eureka_client = eureka_client
        self.client_config = client_config

    def get_instances(self, service_id: str) -> List[ServiceInstance]:
        instance_info = self.eureka_client.get_instances_by_vip_address(service_id, False)
        instances = [EurekaServiceInstance(x) for x in instance_info]
        return instances

    @property
    def services(self) -> List[str]:
        applications = self.eureka_client.get_applications()
        if not applications:
            return []
        registered_apps = applications.get_registered_applications()
        names = []
        for app in registered_apps:
            if not app.get_instances().is_empty():
                names.append(app.get_name().lower())
        return names
