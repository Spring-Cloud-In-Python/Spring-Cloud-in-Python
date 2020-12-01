# -*- coding: utf-8 -*-

__author__ = "Daniel1147 (sxn91401@gmail.com)"
__license__ = "Apache 2.0"

# scip plugin
from eureka.client.app_info import InstanceInfo, LeaseInfo
from eureka.model.instance_info_model import InstanceInfoModel
from eureka.model.lease_info_model import LeaseInfoModel


class TestToModel:
    def setup_method(self):
        self.lease_info_list = [
            LeaseInfo(lease_renewal_interval_in_secs=1, lease_duration_in_secs=1),
            LeaseInfo(lease_renewal_interval_in_secs=2, lease_duration_in_secs=2),
        ]

        self.instance_info_list = [
            InstanceInfo(
                instance_id="instance_id",
                app_name="app_name",
                app_group_name="app_group_name",
                ip_address="127.0.0.1",
                vip_address="stub-service",
                secure_vip_address="stub-service",
                lease_info=self.lease_info_list[0],
                metadata={},
                host_name="localhost",
                action_type=InstanceInfo.ActionType.ADD,
            ),
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
        ]

    def test_lease_info_model(self):
        lease_info_model = LeaseInfoModel.from_entity(self.lease_info_list[0])

        assert lease_info_model.lease_renewal_interval_in_secs == 1

    def test_instance_info_model(self):
        instance_info_model = InstanceInfoModel.from_entity(self.instance_info_list[0])

        assert instance_info_model.instance_id == "instance_id"
        assert instance_info_model.lease_info.lease_renewal_interval_in_secs == 1
        assert instance_info_model.action_type == "ActionType.ADD"


class TestToEntity:
    def setup_method(self):
        self.lease_info_model = LeaseInfoModel(
            **{
                "registration_timestamp": 0,
                "last_renewal_timestamp": 0,
                "eviction_timestamp": 0,
                "service_up_timestamp": 0,
                "lease_renewal_interval_in_secs": 1,
                "lease_duration_in_secs": 1,
            }
        )

        self.instance_info_model = InstanceInfoModel(
            **{
                "instance_id": "instance_id",
                "app_name": "app_name",
                "app_group_name": "app_group_name",
                "ip_address": "127.0.0.1",
                "vip_address": "stub-service",
                "secure_vip_address": "stub-service",
                "metadata": {},
                "last_updated_timestamp": None,
                "last_dirty_timestamp": None,
                "action_type": "ActionType.ADD",
                "host_name": "localhost",
                "is_coordinating_discovery_server": False,
                "is_secure_port_enabled": False,
                "is_unsecure_port_enabled": True,
                "port": 7001,
                "secure_port": 7002,
                "status": "Status.UP",
                "overridden_status": "Status.UNKNOWN",
                "is_instance_info_dirty": False,
                "lease_info": self.lease_info_model,
            }
        )

    def test_lease_info_model(self):
        lease_info = self.lease_info_model.to_entity()

        assert 0 == lease_info.registration_timestamp
        assert 1 == lease_info.lease_renewal_interval_in_secs

    def test_isntance_info_model(self):
        instance_info = self.instance_info_model.to_entity()

        assert instance_info.instance_id == "instance_id"
        assert instance_info.ip_address == "127.0.0.1"
        assert instance_info.status == InstanceInfo.Status.UP
        assert instance_info.last_updated_timestamp is None
        assert instance_info.is_unsecure_port_enabled
        assert instance_info.port == 7001
        assert instance_info.action_type == InstanceInfo.ActionType.ADD
