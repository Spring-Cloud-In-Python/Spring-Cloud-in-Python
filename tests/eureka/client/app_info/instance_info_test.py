# -*- coding: utf-8 -*-

__author__ = "Haribo (haribo1558599@gmail.com)"
__license__ = "Apache 2.0"

# scip plugin
from eureka.client.app_info import InstanceInfo, LeaseInfo
from eureka.utils.timestamp import current_timestamp


class TestInstanceInfo:
    def setup_method(self):
        self.instance_info = InstanceInfo(
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

    def test_is_port_enabled(self):
        assert (
            self.instance_info.is_port_enabled(InstanceInfo.PortType.SECURE)
            == self.instance_info.is_secure_port_enabled
        )
        assert (
            self.instance_info.is_port_enabled(InstanceInfo.PortType.UNSECURE)
            == self.instance_info.is_unsecure_port_enabled
        )

        # If the port type is unknown,it should return False
        assert not self.instance_info.is_port_enabled(None)

    def test_is_dirty(self):
        self.instance_info.is_instance_info_dirty = True
        assert self.instance_info.is_dirty() == self.instance_info.is_instance_info_dirty

        self.instance_info.is_instance_info_dirty = False
        assert self.instance_info.is_dirty() == self.instance_info.is_instance_info_dirty

    def test_set_is_dirty_with_time(self):
        last_dirty_timestamp = self.instance_info.set_is_dirty_with_time()

        assert self.instance_info.is_dirty()
        assert last_dirty_timestamp == self.instance_info.last_dirty_timestamp

    def test_is_dirty_with_time(self):
        if self.instance_info.is_instance_info_dirty:
            assert self.instance_info.is_dirty_with_time() == self.instance_info.last_dirty_timestamp
        else:
            assert self.instance_info.is_dirty_with_time() is None

    def test_unset_is_dirty(self):
        # Unset dirty if unset dirty timestamp >= last dirty timestamp
        self.instance_info.last_dirty_timestamp = current_timestamp()
        unset_dirty_timestamp = self.instance_info.last_dirty_timestamp + 1
        self.instance_info.unset_is_dirty(unset_dirty_timestamp)
        assert not self.instance_info.is_instance_info_dirty

        # Instance will remain dirty if unset dirty timestamp < last dirty timestamp
        self.instance_info.is_instance_info_dirty = True
        self.instance_info.last_dirty_timestamp = 10
        self.instance_info.unset_is_dirty(-1)
        assert self.instance_info.is_instance_info_dirty

    def test_set_status(self):
        self.instance_info.status = InstanceInfo.Status.UNKNOWN
        assert self.instance_info.set_status(InstanceInfo.Status.UP) == InstanceInfo.Status.UNKNOWN

        # If instance's current status is the same as the passing status, it'll return None
        assert self.instance_info.set_status(InstanceInfo.Status.UP) is None
