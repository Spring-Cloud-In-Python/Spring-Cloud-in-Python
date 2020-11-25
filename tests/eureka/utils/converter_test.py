# -*- coding: utf-8 -*-

__author__ = "Daniel1147 (sxn91401@gmail.com)"
__license__ = "Apache 2.0"

# scip plugin
from eureka.client.app_info import InstanceInfo, LeaseInfo
from eureka.client.discovery.shared import Application
from eureka.utils.converter import Decoder, Encoder


class TestEncoder:
    def test_encode_lease_info(self):
        lease_info = LeaseInfo(lease_renewal_interval_in_secs=1, lease_duration_in_secs=1)
        info_dict = Encoder.encode_lease_info(lease_info)

        assert 1 == info_dict["lease_renewal_interval_in_secs"]
        assert 1 == info_dict["lease_duration_in_secs"]
        assert isinstance(info_dict, dict)

    def test_encode_instance(self):
        lease_info = LeaseInfo(lease_renewal_interval_in_secs=1, lease_duration_in_secs=1)

        instance_info = InstanceInfo(
            instance_id="instance_id",
            app_name="app_name",
            app_group_name="app_group_name",
            ip_address="127.0.0.1",
            vip_address="stub-service",
            secure_vip_address="stub-service",
            lease_info=lease_info,
            metadata={},
            host_name="localhost",
        )
        instance_dict = Encoder.encode_instance(instance_info)
        assert "instance_id" == instance_dict["instance_id"]
        assert 1 == instance_dict["lease_info"]["lease_renewal_interval_in_secs"]
        assert isinstance(instance_dict, dict)

    def test_encode_application(self):
        application = Application("example-app")
        instance_info = InstanceInfo(
            instance_id="instance_id",
            app_name="app_name",
            app_group_name="app_group_name",
            ip_address="127.0.0.1",
            vip_address="stub-service",
            secure_vip_address="stub-service",
            lease_info=LeaseInfo(),
            metadata={},
            host_name="localhost",
        )

        instance_2 = InstanceInfo(
            instance_id="instance_id_2",
            app_name="app_name",
            app_group_name="app_group_name",
            ip_address="127.0.0.1",
            vip_address="stub-service-2",
            secure_vip_address="stub-service",
            lease_info=LeaseInfo(),
            metadata={},
            host_name="localhost",
        )

        application.add_instance(instance_info)
        application.add_instance(instance_2)
        application_dict = Encoder.encode_application(application)

        assert "example-app" == application_dict["name"]
        assert application_dict["is_dirty"]
        assert "app_name" == application_dict["instance_dict"][0]["app_name"]

    #
    # def test_encode_applications(self):
    #     assert False


class TestDecoder:
    def test_decode_lease_info(self):
        lease_info_dict = {
            "registration_timestamp": 0,
            "last_renewal_timestamp": 0,
            "eviction_timestamp": 0,
            "service_up_timestamp": 0,
            "lease_renewal_interval_in_secs": 1,
            "lease_duration_in_secs": 1,
        }
        lease_info = Decoder.decode_lease_info(lease_info_dict)

        assert 0 == lease_info.registration_timestamp
        assert 1 == lease_info.lease_renewal_interval_in_secs

    def test_decode_instance(self):
        instance_dict = {
            "instance_id": "instance_id",
            "app_name": "app_name",
            "app_group_name": "app_group_name",
            "ip_address": "127.0.0.1",
            "vip_address": "stub-service",
            "secure_vip_address": "stub-service",
            "metadata": {},
            "last_updated_timestamp": None,
            "last_dirty_timestamp": None,
            "action_type": None,
            "host_name": "localhost",
            "is_coordinating_discovery_server": False,
            "is_secure_port_enabled": False,
            "is_unsecure_port_enabled": True,
            "port": 7001,
            "secure_port": 7002,
            "status": "Status.UP",
            "overridden_status": "Status.UNKNOWN",
            "is_instance_info_dirty": False,
            "lease_info": {
                "registration_timestamp": 0,
                "last_renewal_timestamp": 0,
                "eviction_timestamp": 0,
                "service_up_timestamp": 0,
                "lease_renewal_interval_in_secs": 1,
                "lease_duration_in_secs": 1,
            },
        }
        instance_info = Decoder.decode_instance(instance_dict)

        assert "instance_id" == instance_info.instance_id
        assert "127.0.0.1" == instance_info.ip_address
        assert InstanceInfo.Status.UP == instance_info.status
        assert instance_info.last_updated_timestamp is None
        assert instance_info.is_unsecure_port_enabled
        assert 7001 == instance_info.port

    def test_decode_application(self):
        application_dict = {
            "name": "example-app",
            "is_dirty": False,
            "instance_dict": [
                {
                    "instance_id": "instance_id",
                    "app_name": "app_name",
                    "app_group_name": "app_group_name",
                    "ip_address": "127.0.0.1",
                    "vip_address": "stub-service",
                    "secure_vip_address": "stub-service",
                    "metadata": {},
                    "last_updated_timestamp": None,
                    "last_dirty_timestamp": None,
                    "action_type": None,
                    "host_name": "localhost",
                    "is_coordinating_discovery_server": False,
                    "is_secure_port_enabled": False,
                    "is_unsecure_port_enabled": True,
                    "port": 8787,
                    "secure_port": 7002,
                    "status": "Status.UP",
                    "overridden_status": "Status.UNKNOWN",
                    "is_instance_info_dirty": False,
                    "lease_info": {
                        "registration_timestamp": 0,
                        "last_renewal_timestamp": 0,
                        "eviction_timestamp": 0,
                        "service_up_timestamp": 0,
                        "lease_renewal_interval_in_secs": 30,
                        "lease_duration_in_secs": 90,
                    },
                },
                {
                    "instance_id": "instance_id_2",
                    "app_name": "app_name",
                    "app_group_name": "app_group_name",
                    "ip_address": "127.0.0.1",
                    "vip_address": "stub-service-2",
                    "secure_vip_address": "stub-service",
                    "metadata": {},
                    "last_updated_timestamp": None,
                    "last_dirty_timestamp": None,
                    "action_type": None,
                    "host_name": "localhost",
                    "is_coordinating_discovery_server": False,
                    "is_secure_port_enabled": False,
                    "is_unsecure_port_enabled": True,
                    "port": 7001,
                    "secure_port": 7002,
                    "status": "Status.UP",
                    "overridden_status": "Status.UNKNOWN",
                    "is_instance_info_dirty": False,
                    "lease_info": {
                        "registration_timestamp": 0,
                        "last_renewal_timestamp": 0,
                        "eviction_timestamp": 0,
                        "service_up_timestamp": 0,
                        "lease_renewal_interval_in_secs": 30,
                        "lease_duration_in_secs": 90,
                    },
                },
            ],
        }
        application = Decoder.decode_application(application_dict)

        assert "example-app" == application.name
        assert 2 == application.size()
        assert not application.is_dirty
        assert 8787 == application.get_instance_by_id("instance_id").port

    #
    # def test_decode_applications(self):
    #     assert False
