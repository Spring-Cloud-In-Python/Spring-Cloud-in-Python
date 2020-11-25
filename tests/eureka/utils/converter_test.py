# -*- coding: utf-8 -*-

__author__ = "Daniel1147 (sxn91401@gmail.com)"
__license__ = "Apache 2.0"

# scip plugin
from eureka.client.app_info import InstanceInfo, LeaseInfo
from eureka.utils.converter import Decoder, Encoder


class TestEncoder:
    def test_encode_lease_info(self):
        lease_info = LeaseInfo(lease_renewal_interval_in_secs=1, lease_duration_in_secs=1)
        info_dict = Encoder.encode_lease_info(lease_info)

        assert 1 == info_dict["lease_renewal_interval_in_secs"]
        assert 1 == info_dict["lease_duration_in_secs"]

    def test_encode_instance(self):
        pass
        # instance_info = InstanceInfo(
        #     instance_id="instance_id",
        #     app_name="app_name",
        #     app_group_name="app_group_name",
        #     ip_address="127.0.0.1",
        #     vip_address="stub-service",
        #     secure_vip_address="stub-service",
        #     lease_info=LeaseInfo(),
        #     metadata={},
        #     host_name="localhost",
        # )
        # instance_dict = self.encoder.encode_instance(instance_info)
        # assert "instance_id" == instance_dict["instance_id"]

    # def test_encode_application(self):
    #     assert False
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

    # def test_decode_instance(self):
    #     assert False
    #
    # def test_decode_application(self):
    #     assert False
    #
    # def test_decode_applications(self):
    #     assert False
