# -*- coding: utf-8 -*-

__author__ = "Haribo (haribo1558599@gmail.com)"
__license__ = "Apache 2.0"

# scip plugin
from eureka.client.app_info.instance_info import InstanceInfo
from eureka.client.discovery.discovery_event import DiscoveryEvent


class StatusChangeEvent(DiscoveryEvent):
    def __init__(self, previous_status: InstanceInfo.Status, current_status: InstanceInfo.Status):
        super().__init__()
        self._previous_status = previous_status
        self._current_status = current_status

    @property
    def previous_status(self):
        return self._previous_status

    @property
    def current_status(self):
        return self._current_status

    def is_instance_up(self) -> bool:
        return self._current_status == InstanceInfo.Status.UP

    def __str__(self):
        return (
            "StatusChangeEvent [timestamp="
            + self._timestamp
            + ", current="
            + str(self._current_status.value)
            + ", previous="
            + str(self._previous_status.value)
            + "]"
        )
