# -*- coding: utf-8 -*-

__author__ = "Daniel1147 (sxn91401@gmail.com)"
__license__ = "Apache 2.0"

# scip plugin
from eureka.client.app_info import InstanceInfo, LeaseInfo
from eureka.server.registry.instance_registry import InstanceRegistry


class TestInstanceRegistry:
    def setup_method(self):
        self.instance_info_list = [
            InstanceInfo(
                instance_id="instance_1",
                app_name="app_name",
                app_group_name="app_group_name",
                ip_address="127.0.0.1",
                vip_address="stub-service",
                secure_vip_address="stub-service",
                lease_info=LeaseInfo(),
                metadata={},
                host_name="localhost",
            ),
            InstanceInfo(
                instance_id="instance_2",
                app_name="app_name",
                app_group_name="app_group_name",
                ip_address="127.0.0.1",
                vip_address="stub-service",
                secure_vip_address="stub-service",
                lease_info=LeaseInfo(),
                metadata={},
                host_name="localhost",
            ),
            InstanceInfo(
                instance_id="instance_3",
                app_name="app_2",
                app_group_name="app_group_name",
                ip_address="127.0.0.1",
                vip_address="stub-service",
                secure_vip_address="stub-service",
                lease_info=LeaseInfo(),
                metadata={},
                host_name="localhost",
            ),
        ]
        self.instance_registry = InstanceRegistry()

    def test_register(self):
        self.instance_registry.register(self.instance_info_list[0], 10)

        assert True

    def test_get_application(self):
        self.instance_registry.register(self.instance_info_list[0], 10)
        application = self.instance_registry.get_application("app_name")
        assert application.name == "app_name"
        assert 1 == application.size()

        self.instance_registry.register(self.instance_info_list[1], 10)
        application = self.instance_registry.get_application("app_name")
        assert 2 == application.size()

    def test_get_applications(self):
        self.instance_registry.register(self.instance_info_list[0], 10)
        self.instance_registry.register(self.instance_info_list[1], 10)
        self.instance_registry.register(self.instance_info_list[2], 10)

        applications = self.instance_registry.get_applications()
        assert 3 == applications.size()
        assert 2 == applications.get_registered_application("app_name").size()

        returned_app = applications.get_registered_application("app_2")
        assert 1 == returned_app.size()
        assert "instance_3" == returned_app.get_instance_by_id("instance_3").instance_id
