# -*- coding: utf-8 -*-

__author__ = "Daniel1147 (sxn91401@gmail.com)"
__license__ = "Apache 2.0"

# standard library
import time

# pypi/conda library
from _pytest.monkeypatch import MonkeyPatch

# scip plugin
from eureka.server.lease.lease import Lease


def patch_timestamp(timestamp: int):
    MonkeyPatch().setattr("eureka.server.lease.lease.current_timestamp", lambda: timestamp)


class TestLease:
    class DummyLeaseInfo:
        pass

    def test_initial_lease_not_expired(self):
        dummy_lease_info = self.DummyLeaseInfo()
        lease = Lease(dummy_lease_info, 0)

        assert not lease.is_expired()

    def test_setters(self):
        dummy_lease_info = self.DummyLeaseInfo()
        dummy_lease_info2 = self.DummyLeaseInfo()

        lease = Lease(dummy_lease_info, 0)
        lease.service_up_timestamp = 123

        assert lease.holder != dummy_lease_info2
        assert lease.service_up_timestamp == 123

        lease = Lease(dummy_lease_info2, 0)

        assert lease.holder == dummy_lease_info2

    def test_current_timestamps_should_be_logical(self):
        patch_timestamp(1)
        dummy_lease_info = self.DummyLeaseInfo()
        lease = Lease(dummy_lease_info, 0)

        assert lease.registration_timestamp == 1
        assert lease.last_update_timestamp == 1

    def test_renew(self):
        patch_timestamp(1)
        dummy_lease_info = self.DummyLeaseInfo()
        lease = Lease(dummy_lease_info, 0)

        patch_timestamp(2)
        lease.renew()

        assert lease.registration_timestamp == 1
        assert lease.last_update_timestamp == 2

    def test_cancel(self):
        patch_timestamp(1)
        dummy_lease_info = self.DummyLeaseInfo()
        lease = Lease(dummy_lease_info, 0)

        patch_timestamp(2)
        lease.cancel()

        assert lease.registration_timestamp == 1
        assert lease.eviction_timestamp == 2

    def test_service_up(self):
        patch_timestamp(1)
        dummy_lease_info = self.DummyLeaseInfo()
        lease = Lease(dummy_lease_info, 0)

        patch_timestamp(2)
        lease.service_up()

        assert lease.registration_timestamp == 1
        assert lease.service_up_timestamp == 2

    def test_is_expired(self):
        lease_expire_time_in_secs = 1

        patch_timestamp(1)
        dummy_lease_info = self.DummyLeaseInfo()
        lease = Lease(dummy_lease_info, lease_expire_time_in_secs)

        assert not lease.is_expired()

        patch_timestamp(500)
        assert not lease.is_expired()

        patch_timestamp(1500)
        assert lease.is_expired()
