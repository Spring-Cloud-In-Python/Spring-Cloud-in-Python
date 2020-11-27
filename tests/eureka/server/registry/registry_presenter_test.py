# -*- coding: utf-8 -*-

__author__ = "Daniel1147 (sxn91401@gmail.com)"
__license__ = "Apache 2.0"

# pypi/conda library
from _pytest.monkeypatch import MonkeyPatch

# scip plugin
from eureka.client.app_info import InstanceInfo, LeaseInfo
from eureka.server.registry.instance_registry import InstanceRegistry


class TestRegistryPresenter:
    def setup_method(self):
        MonkeyPatch().setattr("eureka.server.lease.lease.current_timestamp", lambda: 100)
        MonkeyPatch().setattr("eureka.client.app_info.instance_info.current_timestamp", lambda: 200)
        registry = InstanceRegistry()
        registry.register(
            InstanceInfo(
                instance_id="instance_id",
                app_name="app_name",
                app_group_name="app_group_name",
                ip_address="127.0.0.1",
                vip_address="stub-service",
                secure_vip_address="stub-service",
                lease_info=LeaseInfo(),
                metadata={},
                host_name="localhost",
            ),
            10,
        )
        registry.register(
            InstanceInfo(
                instance_id="instance_id_2",
                app_name="app_name",
                app_group_name="app_group_name",
                ip_address="127.0.0.1",
                vip_address="stub-service-2",
                secure_vip_address="stub-service",
                lease_info=LeaseInfo(),
                metadata={},
                host_name="localhost",
            ),
            10,
        )
        registry.register(
            InstanceInfo(
                instance_id="instance_3",
                app_name="app_2",
                app_group_name="app_group_name",
                ip_address="127.0.0.1",
                vip_address="stub-service-2",
                secure_vip_address="stub-service",
                lease_info=LeaseInfo(),
                metadata={},
                host_name="localhost",
            ),
            10,
        )
        self.registry = registry
        self.presenter = registry.get_responser()
        self.application_2_encoded = '{"name": "app_2", "instance_dict": [{"instance_id": "instance_3", "app_name": "app_2", "app_group_name": "app_group_name", "ip_address": "127.0.0.1", "vip_address": "stub-service-2", "secure_vip_address": "stub-service", "metadata": {}, "last_updated_timestamp": 200, "last_dirty_timestamp": null, "action_type": "ActionType.ADD", "host_name": "localhost", "is_coordinating_discovery_server": false, "is_secure_port_enabled": false, "is_unsecure_port_enabled": true, "port": 7001, "secure_port": 7002, "status": "Status.UP", "overridden_status": "Status.UNKNOWN", "lease_info": {"registration_timestamp": 100, "last_renewal_timestamp": 100, "eviction_timestamp": 0, "service_up_timestamp": 100, "lease_renewal_interval_in_secs": 30, "lease_duration_in_secs": 90}}]}'

    def test_query_application(self):
        response = self.presenter.query_application("no_app")

        assert "{}" == response

    def test_query_application(self):
        response = self.presenter.query_application("app_2")

        assert self.application_2_encoded == response

    def test_query_applications(self):
        pass
