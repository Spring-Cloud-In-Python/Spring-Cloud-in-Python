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
        obj = {}
        for property_name in LeaseInfo.__slots__:
            property_key = property_name[1:]  # skip the beginning "_"

            obj[property_key] = getattr(lease_info, property_name)

        return LeaseInfoModel(**obj)

    def to_entity(self) -> LeaseInfo:
        lease_info = LeaseInfo(**self.dict())

        return lease_info
