# -*- coding: utf-8 -*-

__author__ = "Haribo (haribo1558599@gmail.com)"
__license__ = "Apache 2.0"

# scip plugin
from eureka.client.app_info import InstanceInfo, LeaseInfo
from eureka.client.discovery.shared import Application


class TestApplication:
    def setup_method(self):
        self.application = Application("example-app")
        self.instance_info = InstanceInfo(
            instance_id="instance_id",
            app_name="app_name",
            app_group_name="app_group_name",
            ip_address="127.0.0.1",
            vip_address="stub-service",
            secure_vip_address="stub-service",
            lease_info=LeaseInfo(),
            metadata={},
            host_name="localhost",
        )

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
        instance_1 = InstanceInfo(
            instance_id="instance_id_1",
            app_name="app_name",
            app_group_name="app_group_name",
            ip_address="127.0.0.1",
            vip_address="stub-service",
            secure_vip_address="stub-service",
            lease_info=LeaseInfo(),
            metadata={},
            host_name="localhost",
        )
        instance_2 = InstanceInfo(
            instance_id="instance_id_2",
            app_name="app_name",
            app_group_name="app_group_name",
            ip_address="127.0.0.1",
            vip_address="stub-service",
            secure_vip_address="stub-service",
            lease_info=LeaseInfo(),
            metadata={},
            host_name="localhost",
        )

        self.application.add_instance(self.instance_info)
        self.application.add_instance(instance_1)
        self.application.add_instance(instance_2)

        assert self.application.get_all_instances_from_local_cache() == [self.instance_info, instance_1, instance_2]

    def test_shuffle_and_store_instances(self):
        instance_1 = InstanceInfo(
            instance_id="instance_id_1",
            app_name="app_name",
            app_group_name="app_group_name",
            ip_address="127.0.0.1",
            vip_address="stub-service-1",
            secure_vip_address="stub-service",
            lease_info=LeaseInfo(),
            metadata={},
            host_name="localhost",
        )
        instance_2 = InstanceInfo(
            instance_id="instance_id_2",
            app_name="app_name",
            app_group_name="app_group_name",
            ip_address="127.0.0.1",
            vip_address="stub-service-2",
            secure_vip_address="stub-service",
            lease_info=LeaseInfo(),
            metadata={},
            host_name="localhost",
        )

        self.instance_info.set_status(InstanceInfo.Status.UP)
        instance_1.set_status(InstanceInfo.Status.UNKNOWN)
        instance_2.set_status(InstanceInfo.Status.STARTING)

        self.application.add_instance(self.instance_info)
        self.application.add_instance(instance_1)
        self.application.add_instance(instance_2)

        # It should filter out only instances whose status is UP.
        shuffled_and_filtered_instances = self.application.shuffle_and_store_instances(filter_only_up_instances=True)

        assert shuffled_and_filtered_instances == [self.instance_info]

    def test_get_instances(self):
        instance_1 = InstanceInfo(
            instance_id="instance_id_1",
            app_name="app_name",
            app_group_name="app_group_name",
            ip_address="127.0.0.1",
            vip_address="stub-service-1",
            secure_vip_address="stub-service",
            lease_info=LeaseInfo(),
            metadata={},
            host_name="localhost",
        )

        self.application.add_instance(self.instance_info)
        assert self.application.get_instances() == [self.instance_info]

        shuffled_and_filtered_instances = self.application.shuffle_and_store_instances(filter_only_up_instances=True)
        assert self.application.get_instances() == shuffled_and_filtered_instances

        instance_1.set_status(InstanceInfo.Status.STARTING)
        self.application.add_instance(instance_1)
        shuffled_and_filtered_instances = self.application.shuffle_and_store_instances(filter_only_up_instances=True)
        assert self.application.get_instances() == shuffled_and_filtered_instances
