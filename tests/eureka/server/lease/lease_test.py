# -*- coding: utf-8 -*-

__author__ = "Daniel1147 (sxn91401@gmail.com)"
__license__ = "Apache 2.0"

# standard library
import time

# scip plugin
from eureka.server.lease.lease import Lease
from eureka.utils.timestamp import current_timestamp


def equal_with_tolerance(expected, actual):
    tolerance = 50  # tolerant small measurement error
    diff = abs(actual - expected)

    return diff < tolerance


class TestLease:
    class FakeLeaseInfo:
        pass

    def test_initial_lease_not_expired(self):
        fake_lease_info = self.FakeLeaseInfo()
        lease = Lease(fake_lease_info, 0)

        assert not lease.is_expired()

    def test_setters(self):
        fake_lease_info = self.FakeLeaseInfo()
        fake_lease_info2 = self.FakeLeaseInfo()

        lease = Lease(fake_lease_info, 0)
        lease.service_up_timestamp = 123

        assert lease.holder != fake_lease_info2
        assert lease.service_up_timestamp == 123

        lease = Lease(fake_lease_info2, 0)

        assert lease.holder == fake_lease_info2

    def test_current_timestamps_should_be_logical(self):
        start = current_timestamp()

        fake_lease_info = self.FakeLeaseInfo()
        lease = Lease(fake_lease_info, 0)

        assert lease.registration_timestamp >= start <= current_timestamp()
        assert equal_with_tolerance(start, lease.registration_timestamp)
        assert equal_with_tolerance(start, lease.last_update_timestamp)

    def test_renew(self):
        start = current_timestamp()

        fake_lease_info = self.FakeLeaseInfo()
        lease = Lease(fake_lease_info, 0)

        time_passed = 0.1  # pass 0.1 second
        time.sleep(time_passed)
        current = start + time_passed * 1000
        last_update = current
        lease.renew()

        assert equal_with_tolerance(start, lease.registration_timestamp)
        assert equal_with_tolerance(last_update, lease.last_update_timestamp)

    def test_cancel(self):
        start = current_timestamp()

        fake_lease_info = self.FakeLeaseInfo()
        lease = Lease(fake_lease_info, 0)

        time_passed = 0.1  # pass 0.1 second
        time.sleep(time_passed)
        current = start + time_passed * 1000
        cancel_time = current
        lease.cancel()

        assert equal_with_tolerance(start, lease.registration_timestamp)
        assert equal_with_tolerance(cancel_time, lease.eviction_timestamp)

    def test_service_up(self):
        start = current_timestamp()

        fake_lease_info = self.FakeLeaseInfo()
        lease = Lease(fake_lease_info, 0)

        time_passed = 0.1  # pass 0.1 second
        time.sleep(time_passed)
        current = start + time_passed * 1000
        service_uptime = current
        lease.service_up()

        assert equal_with_tolerance(start, lease.registration_timestamp)
        assert equal_with_tolerance(service_uptime, lease.service_up_timestamp)

    def test_is_expired(self):
        lease_expire_time_in_secs = 1

        fake_lease_info = self.FakeLeaseInfo()
        lease = Lease(fake_lease_info, lease_expire_time_in_secs)

        assert not lease.is_expired()

        time_passed = 0.7
        time.sleep(time_passed)
        assert not lease.is_expired()

        time_passed = 0.7
        time.sleep(time_passed)
        assert lease.is_expired()
