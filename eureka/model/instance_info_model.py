# -*- coding: utf-8 -*-
from __future__ import annotations

__author__ = "Daniel1147 (sxn91401@gmail.com)"
__license__ = "Apache 2.0"

# standard library
from enum import Enum
from typing import Dict, Optional

# pypi/conda library
from pydantic import BaseModel

# scip plugin
from eureka.client.app_info.instance_info import InstanceInfo
from eureka.model.lease_info_model import LeaseInfoModel

INSTANCE_INFO_ENUM_TRANSFORM_TABLE = {
    "status": InstanceInfo.Status,
    "overridden_status": InstanceInfo.Status,
    "action_type": InstanceInfo.ActionType,
}


class InstanceInfoModel(BaseModel):
    instance_id: str
    app_name: str
    ip_address: str
    vip_address: str
    secure_vip_address: str
    lease_info: LeaseInfoModel
    host_name: str
    app_group_name: Optional[str]
    metadata: Optional[Dict[str, str]]
    last_updated_timestamp: Optional[int]
    last_dirty_timestamp: Optional[int]
    action_type: Optional[str]
    is_coordinating_discovery_server: Optional[bool]
    is_secure_port_enabled: Optional[bool]
    is_unsecure_port_enabled: Optional[bool]
    port: int = InstanceInfo.DEFAULT_PORT
    secure_port: int = InstanceInfo.DEFAULT_SECURE_PORT
    status: str = InstanceInfo.Status.UP
    overridden_status: str = InstanceInfo.Status.UNKNOWN
    is_instance_info_dirty: Optional[bool]

    @staticmethod
    def from_entity(instance_info: InstanceInfo) -> InstanceInfoModel:
        obj = {}
        property_to_skip = ["_lease_info", "_is_instance_info_dirty"]
        for property_name in instance_info.__slots__:
            if property_name in property_to_skip:
                continue

            property_key = property_name[1:]  # skip the beginning "_"

            value = getattr(instance_info, property_name)
            if isinstance(value, Enum):
                value = str(value)

            obj[property_key] = value

        obj["lease_info"] = LeaseInfoModel.from_entity(instance_info.lease_info)

        return InstanceInfoModel(**obj)

    def to_entity(self) -> InstanceInfo:
        for property_name, enum_type in INSTANCE_INFO_ENUM_TRANSFORM_TABLE.items():
            property_value = getattr(self, property_name)  # e.g. "Status.UP", None

            if property_value is None:
                continue

            property_value = property_value.split(".")[-1]  # e.g. "UP"
            setattr(self, property_name, enum_type(property_value))

        obj = self.dict()
        obj["lease_info"] = self.lease_info.to_entity()
        instance_info = InstanceInfo(**obj)

        return instance_info
