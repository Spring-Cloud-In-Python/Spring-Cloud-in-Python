# -*- coding: utf-8 -*-

__author__ = "Haribo (haribo1558599@gmail.com)"
__license__ = "Apache 2.0"

# scip plugin
from eureka.client.app_info.lease_info import LeaseInfo


def test_lease_info_constructor():
    lease_info = LeaseInfo(lease_renewal_interval_in_secs=-1, lease_duration_in_secs=-1)

    assert lease_info.lease_renewal_interval_in_secs == lease_info.DEFAULT_LEASE_RENEWAL_INTERVAL
    assert lease_info.lease_duration_in_secs == lease_info.DEFAULT_LEASE_DURATION

    lease_info = LeaseInfo(lease_renewal_interval_in_secs=1, lease_duration_in_secs=1)

    assert lease_info.lease_renewal_interval_in_secs == 1
    assert lease_info.lease_duration_in_secs == 1
