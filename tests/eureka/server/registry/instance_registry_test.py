# -*- coding: utf-8 -*-

__author__ = "Daniel1147 (sxn91401@gmail.com)"
__license__ = "Apache 2.0"

# scip plugin
from eureka.server.registry.instance_registry import InstanceRegistry
from tests.eureka.client.discovery.shared.stubs import instance_info
from eureka.server.registry.registry_presenter import RegistryPresenter


class TestInstanceRegistry:
    def setup_method(self):
        self.instance_info_list = [
            instance_info(app_name="app_1", num=1),
            instance_info(app_name="app_1", num=2),
            instance_info(app_name="app_2", num=3),
        ]
        self.instance_registry = InstanceRegistry()

    def test_register(self):
        self.instance_registry.register(self.instance_info_list[0], 10)
        self.instance_registry.register(self.instance_info_list[0], 10)

        assert True

    def test_get_application(self):
        self.instance_registry.register(self.instance_info_list[0], 10)
        application = self.instance_registry.get_application("app_1")
        assert application.name == "app_1"
        assert 1 == application.size()

        self.instance_registry.register(self.instance_info_list[1], 10)
        application = self.instance_registry.get_application("app_1")
        assert 2 == application.size()

    def test_get_absent_application(self):
        application = self.instance_registry.get_application("absent_app")
        assert application is None

        # TODO
        # Here should be another test after implementing registry.cancel():
        # instance_registry.get_application("app") where instances in app have all been cancelled

    def test_get_applications(self):
        self.instance_registry.register(self.instance_info_list[0], 10)
        self.instance_registry.register(self.instance_info_list[1], 10)
        self.instance_registry.register(self.instance_info_list[2], 10)

        applications = self.instance_registry.get_applications()
        assert 3 == applications.size()
        assert 2 == applications.get_registered_application("app_1").size()

        returned_app = applications.get_registered_application("app_2")
        assert 1 == returned_app.size()
        assert "3" == returned_app.get_instance_by_id("3").instance_id

    def test_get_presenter(self):
        assert isinstance(self.instance_registry.get_presenter(), RegistryPresenter)
