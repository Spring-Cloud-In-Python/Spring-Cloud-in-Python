# -*- coding: utf-8 -*-

__author__ = "Ricky"
__license__ = "Apache 2.0"

# scip plugin
from eureka.client.app_info import InstanceInfo, LeaseInfo
from eureka.client.app_info.eureka_instance_config import DefaultEurekaInstanceConfig
from spring_cloud.utils.validate import not_none


class InstanceInfoFactory:
    def create(self, config: DefaultEurekaInstanceConfig):
        lease_info = LeaseInfo(
            lease_renewal_interval_in_secs=config.lease_renewal_interval_in_secs,
            lease_duration_in_secs=config.lease_expiration_duration_in_secs,
        )

        instance_info = InstanceInfo(
            app_name=config.app_name,
            instance_id=config.instance_id,
            ip_address=config.ip_address,
            host_name=config.host_name,
            port=config.unsecure_port,
            is_unsecure_port_enabled=config.is_unsecure_port_enabled,
            secure_port=config.secure_port,
            is_secure_port_enabled=config.is_secure_port_enabled,
            vip_address=config.virtual_host_name,
            secure_vip_address=config.secure_virtual_host_name,
            lease_info=lease_info,
        )

        # Start off with the STARTING state to avoid traffic
        if not config.is_instance_enabled_on_init:
            initial_status = InstanceInfo.Status.STARTING
            instance_info.status = initial_status

        # Add any user-specific metadata information
        metadata_map = config.metadata
        for key in metadata_map:
            if not_none(metadata_map[key]):
                instance_info.metadata[key] = metadata_map[key]

        return instance_info
