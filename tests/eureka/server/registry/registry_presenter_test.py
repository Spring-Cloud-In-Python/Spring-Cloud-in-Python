# -*- coding: utf-8 -*-

__author__ = "Daniel1147 (sxn91401@gmail.com)"
__license__ = "Apache 2.0"

# standard library
from typing import Optional

# pypi/conda library
from _pytest.monkeypatch import MonkeyPatch

# scip plugin
from eureka.client.app_info import InstanceInfo, LeaseInfo
from eureka.client.discovery.shared import Application, Applications
from eureka.server.registry.instance_registry import InstanceRegistry
from eureka.server.registry.registry_presenter import RegistryPresenter


class StubRegistry(InstanceRegistry):
    def __init__(self):
        self.__stub_application = None
        self.__stub_applications = None

    @property
    def stub_application(self):
        return self.__stub_application

    @stub_application.setter
    def stub_application(self, value: Optional[Application]):
        self.__stub_application = value

    @property
    def stub_applications(self):
        return self.__stub_applications

    @stub_applications.setter
    def stub_applications(self, value: Optional[Applications]):
        self.__stub_applications = value

    def get_application(self, application_name: str) -> Application:
        return self.__stub_application

    def get_applications(self) -> Applications:
        return self.__stub_applications


class TestRegistryPresenter:
    def setup_method(self):
        self.stub_registry = StubRegistry()
        self.presenter = RegistryPresenter(self.stub_registry)

    def test_query_absent_application(self):
        self.stub_registry.stub_application = None
        response = self.presenter.query_application("no_app")

        assert response == "{}"

    def test_query_application(self):
        self.stub_registry.stub_application = Application("app_name")
        response = self.presenter.query_application("app_name")

        assert response == '{"name": "app_name", "instance_dict": []}'

    def test_query_applications(self):
        self.stub_registry.stub_applications = Applications()
        response = self.presenter.query_applications()

        assert response == '{"applications": []}'
