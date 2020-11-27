# standard library

# scip plugin
from eureka.client.app_info.instance_info import InstanceInfo
from eureka.client.app_info.lease_info import LeaseInfo
from spring_cloud.eureka.eureka_service_instance import EurekaServiceInstance


def test_eureka_service_instance():
    instance_info0 = InstanceInfo(
        instance_id="0",
        app_name="app0",
        app_group_name="app_group_name",
        ip_address="127.0.0.1",
        vip_address="stub-service",
        secure_vip_address="stub-service",
        lease_info=LeaseInfo(),
        metadata={},
        host_name="localhost",
    )
    instance_info1 = InstanceInfo(
        instance_id="1",
        app_name="app1",
        app_group_name="app_group_name",
        ip_address="127.0.0.1",
        vip_address="stub-service",
        secure_vip_address="stub-service",
        lease_info=LeaseInfo(),
        metadata={},
        host_name="localhost",
    )
    instance_info2 = InstanceInfo(
        instance_id="0",
        app_name="app0",
        app_group_name="app_group_name",
        ip_address="127.0.0.1",
        vip_address="stub-service",
        secure_vip_address="stub-service",
        lease_info=LeaseInfo(),
        metadata={},
        host_name="localhost",
    )

    eureka_service_instance0 = EurekaServiceInstance(instance_info0)
    eureka_service_instance1 = EurekaServiceInstance(instance_info1)
    eureka_service_instance2 = EurekaServiceInstance(instance_info2)

    assert eureka_service_instance0.instance_id() == "0"
    assert eureka_service_instance0.service_id() == "app0"
    assert eureka_service_instance0.secure() is False
    assert EurekaServiceInstance(instance_info0) != instance_info0
    assert EurekaServiceInstance(instance_info0) != instance_info1
    assert eureka_service_instance0 != eureka_service_instance1
    assert eureka_service_instance1 != eureka_service_instance2
    assert eureka_service_instance1 == eureka_service_instance1
