# -*- coding: utf-8 -*-
from __future__ import annotations

__author__ = "Daniel1147 (sxn91401@gmail.com)"
__license__ = "Apache 2.0"

# pypi/conda library
from pydantic import BaseModel

# scip plugin
from eureka.client.app_info import LeaseInfo


class LeaseInfoModel(BaseModel):
    registration_timestamp: int
    last_renewal_timestamp: int
    eviction_timestamp: int
    service_up_timestamp: int
    lease_renewal_interval_in_secs: int
    lease_duration_in_secs: int

    @staticmethod
    def from_entity(lease_info: LeaseInfo) -> LeaseInfoModel:

        return LeaseInfoModel(
            registration_timestamp=lease_info.registration_timestamp,
            last_renewal_timestamp=lease_info.last_renewal_timestamp,
            eviction_timestamp=lease_info.eviction_timestamp,
            service_up_timestamp=lease_info.service_up_timestamp,
            lease_renewal_interval_in_secs=lease_info.lease_renewal_interval_in_secs,
            lease_duration_in_secs=lease_info.lease_duration_in_secs,
        )

    def to_entity(self) -> LeaseInfo:
        lease_info = LeaseInfo(
            registration_timestamp=self.registration_timestamp,
            last_renewal_timestamp=self.last_renewal_timestamp,
            eviction_timestamp=self.eviction_timestamp,
            service_up_timestamp=self.service_up_timestamp,
            lease_renewal_interval_in_secs=self.lease_renewal_interval_in_secs,
            lease_duration_in_secs=self.lease_duration_in_secs,
        )

        return lease_info
