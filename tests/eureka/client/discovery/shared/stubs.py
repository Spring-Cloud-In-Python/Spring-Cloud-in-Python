# -*- coding: utf-8 -*-

# scip plugin
from eureka.client.app_info import InstanceInfo, LeaseInfo

__author__ = "Haribo (haribo1558599@gmail.com)"
__license__ = "Apache 2.0"


def instance_info(app_name: str = "example-app", num: int = 0, vip_address: str = "stub-service", port: int = 7001):
    return InstanceInfo(
        instance_id=str(num),
        app_name=app_name,
        app_group_name="app_group_name",
        ip_address="127.0.0.1",
        vip_address=vip_address,
        secure_vip_address="stub-service",
        lease_info=LeaseInfo(),
        metadata={},
        host_name="localhost",
        port=port,
    )
