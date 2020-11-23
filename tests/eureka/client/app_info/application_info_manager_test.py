# -*- coding: utf-8 -*-

__author__ = "Haribo (haribo1558599@gmail.com)"
__license__ = "Apache 2.0"

# scip plugin
from eureka.client.app_info import ApplicationInfoManager, DefaultEurekaInstanceConfig, InstanceInfo, LeaseInfo


class TestApplicationInfoManager:
    def setup_method(self):
        self.instance = InstanceInfo(
            instance_id="instance_id",
            app_name="example-app-1",
            app_group_name="app_group_name",
            ip_address="127.0.0.1",
            vip_address="stub-service",
            secure_vip_address="stub-service",
            lease_info=LeaseInfo(lease_duration_in_secs=10, lease_renewal_interval_in_secs=20),
            metadata={},
            host_name="localhost",
        )
        self.eureka_instance_config = DefaultEurekaInstanceConfig("example-app-1")

        self.application_info_manager = ApplicationInfoManager(self.eureka_instance_config, self.instance)

    def test_set_instance_status(self):
        self.application_info_manager.set_instance_status(InstanceInfo.Status.DOWN)
        assert self.application_info_manager.instance_info.status == InstanceInfo.Status.DOWN

    def test_refresh_lease_info_if_required(self):
        assert self.eureka_instance_config.lease_expiration_duration_in_secs == LeaseInfo.DEFAULT_LEASE_DURATION
        assert self.eureka_instance_config.lease_renewal_interval_in_secs == LeaseInfo.DEFAULT_LEASE_RENEWAL_INTERVAL

        assert self.instance.lease_info.lease_duration_in_secs != LeaseInfo.DEFAULT_LEASE_DURATION
        assert self.instance.lease_info.lease_renewal_interval_in_secs != LeaseInfo.DEFAULT_LEASE_RENEWAL_INTERVAL

        self.application_info_manager.refresh_lease_info_if_required()
        assert self.application_info_manager.instance_info.is_dirty()
        assert (
            self.application_info_manager.instance_info.lease_info.lease_duration_in_secs
            == LeaseInfo.DEFAULT_LEASE_DURATION
        )
        assert self.instance.lease_info.lease_renewal_interval_in_secs == LeaseInfo.DEFAULT_LEASE_RENEWAL_INTERVAL
