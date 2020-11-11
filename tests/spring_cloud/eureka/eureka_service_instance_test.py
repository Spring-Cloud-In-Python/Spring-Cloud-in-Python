# scip plugin
from spring_cloud.spring_cloud.eureka.eureka_service_instance import EurekaServiceInstance


def test_cal():
    eureka_service_instance = EurekaServiceInstance()
    instance_info = eureka_service_instance.get_instance_info()
