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
from eureka.client.app_info import LeaseInfo
from eureka.client.app_info.instance_info import InstanceInfo
from eureka.model.lease_info_model import LeaseInfoModel

INSTANCE_INFO_ENUM_TRANSFORM_TABLE = {
    "status": InstanceInfo.Status,
    "overridden_status": InstanceInfo.Status,
    "action_type": InstanceInfo.ActionType,
}

DEFAULT_LEASE_INFO_MODEL = LeaseInfoModel.from_entity(LeaseInfo())


def enum_value_if_not_none(enum):
    return enum.value if enum is not None else None


class InstanceInfoModel(BaseModel):
    instance_id: str
    app_name: str
    ip_address: str
    vip_address: str
    secure_vip_address: str
    lease_info: LeaseInfoModel = DEFAULT_LEASE_INFO_MODEL
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
    status: str = InstanceInfo.Status.UP.value
    overridden_status: str = InstanceInfo.Status.UNKNOWN.value
    is_instance_info_dirty: Optional[bool]

    @staticmethod
    def from_entity(instance_info: InstanceInfo) -> InstanceInfoModel:
        return InstanceInfoModel(
            instance_id=instance_info.instance_id,
            app_name=instance_info.app_name,
            ip_address=instance_info.ip_address,
            vip_address=instance_info.vip_address,
            secure_vip_address=instance_info.secure_vip_address,
            lease_info=LeaseInfoModel.from_entity(instance_info.lease_info),
            host_name=instance_info.host_name,
            app_group_name=instance_info.app_group_name,
            metadata=instance_info.metadata,
            last_updated_timestamp=instance_info.last_updated_timestamp,
            last_dirty_timestamp=instance_info.last_dirty_timestamp,
            action_type=enum_value_if_not_none(instance_info.action_type),
            is_coordinating_discovery_server=instance_info.is_coordinating_discovery_server,
            is_secure_port_enabled=instance_info.is_secure_port_enabled,
            is_unsecure_port_enabled=instance_info.is_unsecure_port_enabled,
            port=instance_info.port,
            secure_port=instance_info.secure_port,
            status=enum_value_if_not_none(instance_info.status),
            overridden_status=enum_value_if_not_none(instance_info.overridden_status),
            is_instance_info_dirty=instance_info.is_instance_info_dirty,
        )

    def to_entity(self) -> InstanceInfo:
        return InstanceInfo(
            instance_id=self.instance_id,
            app_name=self.app_name,
            ip_address=self.ip_address,
            vip_address=self.vip_address,
            secure_vip_address=self.secure_vip_address,
            lease_info=self.lease_info.to_entity(),
            host_name=self.host_name,
            app_group_name=self.app_group_name,
            metadata=self.metadata,
            last_updated_timestamp=self.last_updated_timestamp,
            last_dirty_timestamp=self.last_dirty_timestamp,
            action_type=InstanceInfo.ActionType(self.action_type) if self.action_type is not None else None,
            is_coordinating_discovery_server=self.is_coordinating_discovery_server,
            is_secure_port_enabled=self.is_secure_port_enabled,
            is_unsecure_port_enabled=self.is_unsecure_port_enabled,
            port=self.port,
            secure_port=self.secure_port,
            status=InstanceInfo.Status(self.status),
            overridden_status=InstanceInfo.Status(self.overridden_status),
            is_instance_info_dirty=self.is_instance_info_dirty,
        )
