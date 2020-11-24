# -*- coding: utf-8 -*-

# standard library
import random
import threading
from typing import List, Optional

# scip plugin
from eureka.client.app_info.instance_info import InstanceInfo

__author__ = "Haribo (haribo1558599@gmail.com)"
__license__ = "Apache 2.0"


class Application:
    """
    The application class holds the list of instances for a particular
    application.

    See com.netflix.discovery.shared.Application.
    """

    def __init__(self, name: str):
        super().__init__()
        self._name = name
        self._is_dirty = False
        self._shuffled_and_filtered_instances = None
        self._instance_dict = {}
        self._instances_lock = threading.RLock()

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, name: str):
        self._name = name

    @property
    def is_dirty(self):
        return self._is_dirty

    def size(self) -> int:
        return len(self._instance_dict)

    def add_instance(self, instance_info: InstanceInfo):
        self._instance_dict[instance_info.instance_id] = instance_info
        self._is_dirty = True

    def remove_instance(self, instance_info: InstanceInfo, mark_as_dirty: bool = True):
        self._instance_dict.pop(instance_info.instance_id, None)
        if mark_as_dirty:
            self._is_dirty = True

    def get_instance_by_id(self, instance_id: str) -> Optional[InstanceInfo]:
        return self._instance_dict.get(instance_id, None)

    def get_instances(self) -> Optional[List[InstanceInfo]]:
        """
        Note that the instances are always returned with random order after
        shuffling to avoid traffic to the same instances during startup. The
        shuffling always happens once after every fetch cycle as specified in
        EurekaClientConfig getRegistryFetchIntervalSeconds().
        """
        return (
            self._shuffled_and_filtered_instances
            if self._shuffled_and_filtered_instances
            else self.get_all_instances_from_local_cache()
        )

    def get_all_instances_from_local_cache(self) -> List[InstanceInfo]:
        """
        Gets the list of non-shuffled and non-filtered instances associated with
        this particular application.
        """
        return list(dict.values(self._instance_dict))

    def shuffle_and_store_instances(self, filter_only_up_instances: bool) -> List[InstanceInfo]:
        self._shuffled_and_filtered_instances = self.get_all_instances_from_local_cache()

        # We will filter out instances whose status are UP.
        if filter_only_up_instances:
            self._shuffled_and_filtered_instances = list(
                filter(
                    lambda instance: instance.status == InstanceInfo.Status.UP, self._shuffled_and_filtered_instances,
                )
            )

        if self._shuffled_and_filtered_instances:
            random.shuffle(self._shuffled_and_filtered_instances)

        return self._shuffled_and_filtered_instances
