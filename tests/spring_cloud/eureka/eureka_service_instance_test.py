# standard library
from unittest.mock import Mock

# scip plugin
from spring_cloud.spring_cloud.eureka.eureka_service_instance import EurekaServiceInstance


def test_eureka_service_instance():
    instance_info0 = Mock()
    instance_info0.id = 0
    instance_info0.app_name = "app0"
    instance_info1 = Mock()
    instance_info1.id = 1
    instance_info1.app_name = "app1"
    instance_info2 = Mock()
    instance_info2.id = 0
    instance_info2.app_name = "app0"

    eureka_service_instance0 = EurekaServiceInstance(instance_info0)
    eureka_service_instance1 = EurekaServiceInstance(instance_info1)
    eureka_service_instance2 = EurekaServiceInstance(instance_info2)

    instance_info = eureka_service_instance0.get_instance_info()
    assert eureka_service_instance0.instance_id() == instance_info.get_id()
    assert eureka_service_instance0.service_id() == instance_info.get_app_name()
    assert EurekaServiceInstance(instance_info0) != instance_info0
    assert EurekaServiceInstance(instance_info0) != instance_info1
    assert eureka_service_instance0 != eureka_service_instance1
    assert eureka_service_instance1 != eureka_service_instance2
    assert eureka_service_instance1 == eureka_service_instance1
