# -*- coding: utf-8 -*-

__author__ = "Ricky"
__license__ = "Apache 2.0"

# standard library
from typing import List, Set

# scip plugin
from spring_cloud.commons.client.discovery.discovery_client import DiscoveryClient
from spring_cloud.commons.client.service_instance import ServiceInstance
from spring_cloud.spring_cloud.eureka.eureka_service_instance import EurekaServiceInstance


class EurekaDiscoveryClient(DiscoveryClient):
    def __init__(self, eureka_client, client_config):
        self.DESCRIPTION = "Spring Cloud Eureka Discovery Client"
        self.eureka_client = eureka_client
        self.client_config = client_config

    def get_instances(self, service_id: str) -> List[ServiceInstance]:
        infos = self.eureka_client.getInstancesByVipAddress(service_id, False)
        instances = [EurekaServiceInstance(x) for x in infos]
        return instances

    def services(self) -> List[str]:
        applications = self.eureka_client.getApplications()
        if not applications:
            return []
        registered = applications.getRegisteredApplications()
        names = []
        for app in registered:
            if app.getInstances().isEmpty():
                continue
            names.append(app.getName().toLowerCase())
        return names
