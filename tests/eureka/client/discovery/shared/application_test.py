# -*- coding: utf-8 -*-

__author__ = "Haribo (haribo1558599@gmail.com)"
__license__ = "Apache 2.0"

# scip plugin
from eureka.client.app_info.instance_info import InstanceInfo
from eureka.client.discovery.shared.application import Application
from tests.eureka.client.discovery.shared.stubs import instance_info


class TestApplication:
    def setup_method(self):
        self.application = Application("example-app")
        self.instance_info = instance_info()
        self.instance_info_1 = instance_info(num=1)
        self.instance_info_2 = instance_info(num=2)

    def test_add_and_get_instance(self):
        self.application.add_instance(self.instance_info)

        assert self.application.size() == 1
        assert self.application.is_dirty
        assert self.application.get_instance_by_id(self.instance_info.instance_id) == self.instance_info

    def test_remove_instance(self):
        self.application.add_instance(self.instance_info)
        self.application.remove_instance(self.instance_info)

        assert self.application.size() == 0
        assert self.application.is_dirty

    def test_get_all_instances_from_local_cache(self):
        self.application.add_instance(self.instance_info)
        self.application.add_instance(self.instance_info_1)
        self.application.add_instance(self.instance_info_2)

        assert self.application.get_all_instances_from_local_cache() == [
            self.instance_info,
            self.instance_info_1,
            self.instance_info_2,
        ]

    def test_shuffle_and_store_instances(self):
        self.instance_info.set_status(InstanceInfo.Status.UP)
        self.instance_info_1.set_status(InstanceInfo.Status.UNKNOWN)
        self.instance_info_2.set_status(InstanceInfo.Status.STARTING)

        self.application.add_instance(self.instance_info)
        self.application.add_instance(self.instance_info_1)
        self.application.add_instance(self.instance_info_2)

        # It should filter out only instances whose status is UP.
        shuffled_and_filtered_instances = self.application.shuffle_and_store_instances(filter_only_up_instances=True)

        assert shuffled_and_filtered_instances == [self.instance_info]

    def test_get_instances(self):
        self.application.add_instance(self.instance_info)
        assert self.application.get_instances() == [self.instance_info]

        shuffled_and_filtered_instances = self.application.shuffle_and_store_instances(filter_only_up_instances=True)
        assert self.application.get_instances() == shuffled_and_filtered_instances

        self.instance_info_1.set_status(InstanceInfo.Status.STARTING)
        self.application.add_instance(self.instance_info_1)
        shuffled_and_filtered_instances = self.application.shuffle_and_store_instances(filter_only_up_instances=True)
        assert self.application.get_instances() == shuffled_and_filtered_instances
