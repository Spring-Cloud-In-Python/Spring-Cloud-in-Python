# scip plugin
from spring_cloud.spring_cloud.eureka.eureka_service_instance import EurekaServiceInstance
from tests.spring_cloud.eureka.instanceinfo import InstanceInfo


def test_eureka_service_instance():
    instance_info0 = InstanceInfo(1, "app1")
    instance_info1 = InstanceInfo(1, "app2")
    instance_info2 = InstanceInfo(1, "app3")
    eureka_service_instance = EurekaServiceInstance(instance_info0)
    eureka_service_instance1 = EurekaServiceInstance(instance_info1)
    eureka_service_instance2 = EurekaServiceInstance(instance_info2)
    instance_info = eureka_service_instance.get_instance_info()
    assert eureka_service_instance.instance_id() == instance_info.get_id() == 1
    assert eureka_service_instance.service_id() == instance_info.get_app_name() == "app1"
    assert eureka_service_instance.host() == instance_info.get_host_name() == "host_name"
    assert EurekaServiceInstance(instance_info0) != instance_info1
    assert eureka_service_instance != eureka_service_instance1
    assert eureka_service_instance1 != eureka_service_instance2
    assert eureka_service_instance1 == eureka_service_instance1
    assert not eureka_service_instance.secure()
