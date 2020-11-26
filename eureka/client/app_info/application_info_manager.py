# -*- coding: utf-8 -*-
# standard library
from abc import ABC, abstractmethod

# scip plugin
from eureka.client.app_info.eureka_instance_config import EurekaInstanceConfig
from eureka.client.app_info.instance_info import InstanceInfo
from eureka.client.app_info.lease_info import LeaseInfo
from eureka.client.discovery.status_change_event import StatusChangeEvent

__author__ = "Haribo (haribo1558599@gmail.com)"
__license__ = "Apache 2.0"


class ApplicationInfoManager:
    def __init__(self, eureka_instance_config: EurekaInstanceConfig, instance_info: InstanceInfo):
        self._eureka_instance_config = eureka_instance_config
        self._instance_info = instance_info
        self._listener_name_to_listener_dict = {}

    class StatusChangeListener(ABC):
        def __init__(self, name: str):
            self._name = name

        @property
        def name(self) -> str:
            return self._name

        @abstractmethod
        def notify(self, status_change_event: StatusChangeEvent):
            raise NotImplemented

    @property
    def eureka_instance_config(self) -> EurekaInstanceConfig:
        return self._eureka_instance_config

    @property
    def instance_info(self) -> InstanceInfo:
        return self._instance_info

    def set_instance_status(self, status: InstanceInfo.Status):
        previous_status = self._instance_info.set_status(status)

        if previous_status:
            for listener in self._listener_name_to_listener_dict.values():
                try:
                    listener.notify(StatusChangeEvent(previous_status, status))
                except Exception as e:
                    print(f"Failed to notify listener: {listener.name}", e)

    def register_status_change_listener(self, listener: StatusChangeListener):
        self._listener_name_to_listener_dict[listener.name] = listener

    def unregister_status_change_listener(self, listener_name: str):
        self._listener_name_to_listener_dict.pop(listener_name, None)

    def refresh_lease_info_if_required(self):
        lease_info = self._instance_info.lease_info

        if lease_info:
            current_lease_duration_in_secs = self._eureka_instance_config.lease_expiration_duration_in_secs
            current_lease_renewal_interval_in_secs = self._eureka_instance_config.lease_renewal_interval_in_secs

            if (
                lease_info.lease_duration_in_secs != current_lease_duration_in_secs
                or lease_info.lease_renewal_interval_in_secs != current_lease_renewal_interval_in_secs
            ):
                self._instance_info.lease_info = LeaseInfo(
                    lease_duration_in_secs=current_lease_duration_in_secs,
                    last_renewal_timestamp=current_lease_renewal_interval_in_secs,
                )
                self._instance_info.set_is_dirty()
