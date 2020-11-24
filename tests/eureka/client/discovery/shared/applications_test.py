# -*- coding: utf-8 -*-

__author__ = "Haribo (haribo1558599@gmail.com)"
__license__ = "Apache 2.0"

# scip plugin
from eureka.client.app_info.instance_info import InstanceInfo
from eureka.client.app_info.lease_info import LeaseInfo
from eureka.client.discovery.shared.application import Application
from eureka.client.discovery.shared.applications import Applications


class TestApplication:
    def setup_method(self):
        self.applications = Applications()

        self.instance_0 = InstanceInfo(
            instance_id="instance_id",
            app_name="example-app-1",
            app_group_name="app_group_name",
            ip_address="127.0.0.1",
            vip_address="stub-service",
            secure_vip_address="stub-service",
            lease_info=LeaseInfo(),
            metadata={},
            host_name="localhost",
        )
        self.instance_1 = InstanceInfo(
            instance_id="instance_id_1",
            app_name="example-app-1",
            app_group_name="app_group_name",
            ip_address="127.0.0.1",
            vip_address="stub-service",
            secure_vip_address="stub-service",
            lease_info=LeaseInfo(),
            metadata={},
            host_name="localhost",
        )
        self.instance_2 = InstanceInfo(
            instance_id="instance_id_2",
            app_name="example-app-2",
            app_group_name="app_group_name",
            ip_address="127.0.0.1",
            vip_address="stub-service-2",
            secure_vip_address="stub-service",
            lease_info=LeaseInfo(),
            metadata={},
            host_name="localhost",
        )

        self.application_1 = Application("example-app-1")
        self.application_1.add_instance(self.instance_0)
        self.application_1.add_instance(self.instance_1)

        self.application_2 = Application("example-app-2")
        self.application_2.add_instance(self.instance_2)

        self.applications.add_application(self.application_1)
        self.applications.add_application(self.application_2)

    def test_get_instances_by_virtual_host_name(self):
        instances = self.applications.get_instances_by_virtual_host_name("stub-service")

        assert instances.next() == self.instance_0
        assert instances.next() == self.instance_1

    def test_size(self):
        assert self.applications.size() == 3

    def test_shuffle_instances_and_filter_only_up_instances(self):
        self.instance_0.set_status(InstanceInfo.Status.UP)
        self.instance_1.set_status(InstanceInfo.Status.UNKNOWN)
        self.instance_2.set_status(InstanceInfo.Status.UP)

        self.applications.shuffle_instances(filter_only_up_instances=True)

        instances = self.applications.get_instances_by_virtual_host_name("stub-service")
        assert instances.next().instance_id == self.instance_0.instance_id
        assert instances.next().instance_id == self.instance_0.instance_id

        instances = self.applications.get_instances_by_virtual_host_name("stub-service-2")
        assert instances.next().instance_id == self.instance_2.instance_id
        assert instances.next().instance_id == self.instance_2.instance_id

    def test_shuffle_instances_and_get_all_instances(self):
        self.instance_0.set_status(InstanceInfo.Status.UP)
        self.instance_1.set_status(InstanceInfo.Status.UNKNOWN)
        self.instance_2.set_status(InstanceInfo.Status.STARTING)

        self.applications.shuffle_instances(filter_only_up_instances=False)

        instances = self.applications.get_instances_by_virtual_host_name("stub-service")
        assert instances.next().instance_id == self.instance_0.instance_id
        assert instances.next().instance_id == self.instance_1.instance_id
        assert instances.next().instance_id == self.instance_0.instance_id

        instances = self.applications.get_instances_by_virtual_host_name("stub-service-2")
        assert instances.next().instance_id == self.instance_2.instance_id
        assert instances.next().instance_id == self.instance_2.instance_id

    def test_compute_reconciliation_hash_code(self):
        self.instance_0.set_status(InstanceInfo.Status.DOWN)
        self.instance_1.set_status(InstanceInfo.Status.UNKNOWN)
        self.instance_2.set_status(InstanceInfo.Status.STARTING)
        assert self.applications.compute_reconciliation_hash_code() == "DOWN_1_STARTING_1_UNKNOWN_1_"

        self.instance_0.set_status(InstanceInfo.Status.DOWN)
        self.instance_1.set_status(InstanceInfo.Status.DOWN)
        self.instance_2.set_status(InstanceInfo.Status.STARTING)
        assert self.applications.compute_reconciliation_hash_code() == "DOWN_2_STARTING_1_"

        self.instance_0.set_status(InstanceInfo.Status.OUT_OF_SERVICE)
        self.instance_1.set_status(InstanceInfo.Status.OUT_OF_SERVICE)
        self.instance_2.set_status(InstanceInfo.Status.OUT_OF_SERVICE)
        assert self.applications.compute_reconciliation_hash_code() == "OUT_OF_SERVICE_3_"
