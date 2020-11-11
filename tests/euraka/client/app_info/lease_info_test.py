# -*- coding: utf-8 -*-

__author__ = "Haribo (haribo1558599@gmail.com)"
__license__ = "Apache 2.0"

# scip plugin
from eureka.client.app_info.lease_info import LeaseInfo


def test_lease_info():
    lease_info = LeaseInfo(registration_timestamp=10)
    assert lease_info.registration_timestamp == 10
