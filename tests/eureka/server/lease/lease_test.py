# -*- coding: utf-8 -*-

__author__ = "Daniel1147 (sxn91401@gmail.com)"
__license__ = "Apache 2.0"

# standard library
from datetime import datetime

# scip plugin
from spring_cloud.eureka.server.lease.lease import Lease


class FakeLeaseInfo:
    pass


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
    start = datetime.now().microsecond

    fake_lease_info = FakeLeaseInfo()
    lease = Lease(fake_lease_info, 0)
    assert lease.registration_timestamp >= start <= datetime.now().microsecond
