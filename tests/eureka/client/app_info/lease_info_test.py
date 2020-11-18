# -*- coding: utf-8 -*-

__author__ = "Haribo (haribo1558599@gmail.com)"
__license__ = "Apache 2.0"

# scip plugin
from eureka.client.app_info.lease_info import LeaseInfo


def test_init_lease_info_with_valid_times():
    lease_info = LeaseInfo(lease_renewal_interval_in_secs=1, lease_duration_in_secs=1)

    assert lease_info.lease_renewal_interval_in_secs == 1
    assert lease_info.lease_duration_in_secs == 1


def test_init_lease_info_with_invalid_times_should_be_replaced_with_default_values():
    lease_info = LeaseInfo(lease_renewal_interval_in_secs=-1, lease_duration_in_secs=-1)

    assert lease_info.lease_renewal_interval_in_secs == lease_info.DEFAULT_LEASE_RENEWAL_INTERVAL
    assert lease_info.lease_duration_in_secs == lease_info.DEFAULT_LEASE_DURATION
