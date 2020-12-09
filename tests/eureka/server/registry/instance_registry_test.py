# -*- coding: utf-8 -*-

__author__ = "Daniel1147 (sxn91401@gmail.com)"
__license__ = "Apache 2.0"

# scip plugin
from eureka.server.registry.instance_registry import InstanceRegistry
from eureka.server.registry.registry_presenter import RegistryPresenter
from tests.eureka.client.discovery.shared.stubs import instance_info

LEASE_DURATION = 10


class TestInstanceRegistry:
    def setup_method(self):
        self.instance_info_list = [
            instance_info(app_name="app_1", num=1),
            instance_info(app_name="app_1", num=2),
            instance_info(app_name="app_2", num=3),
        ]
        self.instance_registry = InstanceRegistry()

    def test_register_and_cancel(self):
        # Test for registering.
        self.instance_registry.register(self.instance_info_list[0], LEASE_DURATION)
        self.instance_registry.register(self.instance_info_list[1], LEASE_DURATION)
        self.instance_registry.register(self.instance_info_list[2], LEASE_DURATION)
        assert 2 == self.instance_registry.get_application("app_1").size()
        assert 1 == self.instance_registry.get_application("app_2").size()

        # Test for simple cancellation.
        result = self.instance_registry.cancel(
            self.instance_info_list[0].app_name, self.instance_info_list[0].instance_id
        )
        assert 1 == self.instance_registry.get_application("app_1").size()
        assert result

        # The second cancellation of the instance should return False and make no change to the registry.
        result = self.instance_registry.cancel(
            self.instance_info_list[0].app_name, self.instance_info_list[0].instance_id
        )
        assert 1 == self.instance_registry.get_application("app_1").size()
        assert not result

        # Test for adding the instance which has been removed before.
        self.instance_registry.register(self.instance_info_list[0], LEASE_DURATION)
        assert 2 == self.instance_registry.get_application("app_1").size()

        result = self.instance_registry.cancel(
            self.instance_info_list[2].app_name, self.instance_info_list[2].instance_id
        )
        assert self.instance_registry.get_application("app_2") is None
        assert result

        # Test for the cancellation of an application does not affect the remain applications.
        applications = self.instance_registry.get_applications()
        assert applications.size() == 2
        assert applications.get_registered_application(self.instance_info_list[1].app_name).name == "app_1"
        assert applications.get_registered_application(self.instance_info_list[2].app_name) is None

    def test_get_application(self):
        self.instance_registry.register(self.instance_info_list[0], LEASE_DURATION)
        application = self.instance_registry.get_application("app_1")
        assert application.name == "app_1"
        assert 1 == application.size()

        self.instance_registry.register(self.instance_info_list[1], LEASE_DURATION)
        application = self.instance_registry.get_application("app_1")
        assert 2 == application.size()

    def test_get_absent_application(self):
        application = self.instance_registry.get_application("absent_app")
        assert application is None

        instance_info_sample = self.instance_info_list[0]
        self.instance_registry.register(instance_info_sample, LEASE_DURATION)
        self.instance_registry.cancel(instance_info_sample.app_name, instance_info_sample.instance_id)
        assert self.instance_registry.get_application(instance_info_sample.app_name) is None

    def test_get_applications(self):
        self.instance_registry.register(self.instance_info_list[0], LEASE_DURATION)
        self.instance_registry.register(self.instance_info_list[1], LEASE_DURATION)
        self.instance_registry.register(self.instance_info_list[2], LEASE_DURATION)

        applications = self.instance_registry.get_applications()
        assert 3 == applications.size()
        assert 2 == applications.get_registered_application("app_1").size()

        returned_app = applications.get_registered_application("app_2")
        assert 1 == returned_app.size()
        assert "3" == returned_app.get_instance_by_id("3").instance_id

    def test_get_presenter(self):
        assert isinstance(self.instance_registry.get_presenter(), RegistryPresenter)
