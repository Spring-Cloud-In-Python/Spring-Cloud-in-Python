# -*- coding: utf-8 -*-

__author__ = "Daniel1147 (sxn91401@gmail.com)"
__license__ = "Apache 2.0"

# standard library
import time

# scip plugin
from spring_cloud.commons.utils.timestamp import current_timestamp
from spring_cloud.eureka.server.lease.lease import Lease


class FakeLeaseInfo:
    pass


def equal_with_tolerance(expected, actual, tolerance):
    diff = abs(actual - expected)
    if diff < tolerance:
        return True

    return False


def assert_timestamp(lease, expected):
    tolerance = 50  # tolerant small measurement error
    for k, v in expected.items():
        assert equal_with_tolerance(v, getattr(lease, k), tolerance)


def test_expired_at_first():
    fake_lease_info = FakeLeaseInfo()
    lease = Lease(fake_lease_info, 0)

    assert not lease.is_expired()


def test_setters():
    fake_lease_info = FakeLeaseInfo()
    fake_lease_info2 = FakeLeaseInfo()

    lease = Lease(fake_lease_info, 0)
    lease.service_up_timestamp = 123

    assert lease.holder != fake_lease_info2
    assert lease.service_up_timestamp == 123

    lease = Lease(fake_lease_info2, 0)

    assert lease.holder == fake_lease_info2


def test_timestamps():
    start = current_timestamp()

    fake_lease_info = FakeLeaseInfo()
    lease = Lease(fake_lease_info, 0)

    expected = {"registration_timestamp": start, "last_update_timestamp": start}
    assert lease.registration_timestamp >= start <= current_timestamp()
    assert_timestamp(lease, expected)


def test_renew():
    start = current_timestamp()

    fake_lease_info = FakeLeaseInfo()
    lease = Lease(fake_lease_info, 0)

    time_passed = 0.1  # pass 0.1 second
    time.sleep(time_passed)
    current = start + time_passed * 1000
    last_update = current
    lease.renew()

    expected = {"registration_timestamp": start, "last_update_timestamp": last_update}
    assert_timestamp(lease, expected)


def test_cancel():
    start = current_timestamp()

    fake_lease_info = FakeLeaseInfo()
    lease = Lease(fake_lease_info, 0)

    time_passed = 0.1  # pass 0.1 second
    time.sleep(time_passed)
    current = start + time_passed * 1000
    cancel_time = current
    lease.cancel()

    expected = {"registration_timestamp": start, "eviction_timestamp": cancel_time}
    assert_timestamp(lease, expected)
