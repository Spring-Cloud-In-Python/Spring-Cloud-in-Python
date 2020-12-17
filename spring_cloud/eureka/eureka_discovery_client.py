# -*- coding: utf-8 -*-
# scip plugin
from eureka.client.discovery import EurekaClientConfig

__author__ = "Ricky"
__license__ = "Apache 2.0"

# standard library
from typing import List

# scip plugin
from spring_cloud.commons.client.discovery.discovery_client import DiscoveryClient
from spring_cloud.commons.client.service_instance import ServiceInstance
from spring_cloud.eureka.eureka_service_instance import EurekaServiceInstance


class EurekaDiscoveryClient(DiscoveryClient):
    def __init__(self, eureka_client: EurekaClient):
        self.DESCRIPTION = "Spring Cloud Eureka Discovery Client"
        self.eureka_client = eureka_client

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
        return [app.get_name().lower() for app in registered_apps if not app.get_instances().is_empty()]
