# -*- coding: utf-8 -*-

__author__ = "Daniel1147 (sxn91401@gmail.com)"
__license__ = "Apache 2.0"

# scip plugin
from eureka.client.app_info import InstanceInfo, LeaseInfo
from eureka.client.discovery.shared import Application, Applications
from eureka.model.application_model import ApplicationModel
from eureka.model.applications_model import ApplicationsModel
from eureka.model.instance_info_model import InstanceInfoModel
from eureka.model.lease_info_model import LeaseInfoModel
from tests.eureka.client.discovery.shared.stubs import instance_info


def lease_info_model_template(
    registration_timestamp=0,
    last_renewal_timestamp=0,
    eviction_timestamp=0,
    service_up_timestamp=0,
    lease_renewal_interval_in_secs=1,
    lease_duration_in_secs=1,
) -> LeaseInfoModel:
    return LeaseInfoModel(
        registration_timestamp=registration_timestamp,
        last_renewal_timestamp=last_renewal_timestamp,
        eviction_timestamp=eviction_timestamp,
        service_up_timestamp=service_up_timestamp,
        lease_renewal_interval_in_secs=lease_renewal_interval_in_secs,
        lease_duration_in_secs=lease_duration_in_secs,
    )


def instance_info_model_template(
    instance_id,
    app_name,
    app_group_name="app_group_name",
    ip_address="127.0.0.1",
    vip_address="stub-service",
    secure_vip_address="stub-service",
    metadata=None,
    last_updated_timestamp=None,
    last_dirty_timestamp=None,
    action_type=None,
    host_name="localhost",
    is_coordinating_discovery_server=False,
    is_secure_port_enabled=False,
    is_unsecure_port_enabled=True,
    port=7001,
    secure_port=7002,
    status="UP",
    overridden_status="UNKNOWN",
    is_instance_info_dirty=False,
    lease_info=None,
) -> InstanceInfoModel:
    if metadata is None:
        metadata = {}

    if lease_info is None:
        lease_info = lease_info_model_template()

    return InstanceInfoModel(
        instance_id=instance_id,
        app_name=app_name,
        app_group_name=app_group_name,
        ip_address=ip_address,
        vip_address=vip_address,
        secure_vip_address=secure_vip_address,
        metadata=metadata,
        last_updated_timestamp=last_updated_timestamp,
        last_dirty_timestamp=last_dirty_timestamp,
        action_type=action_type,
        host_name=host_name,
        is_coordinating_discovery_server=is_coordinating_discovery_server,
        is_secure_port_enabled=is_secure_port_enabled,
        is_unsecure_port_enabled=is_unsecure_port_enabled,
        port=port,
        secure_port=secure_port,
        status=status,
        overridden_status=overridden_status,
        is_instance_info_dirty=is_instance_info_dirty,
        lease_info=lease_info,
    )


class TestToModel:
    def setup_method(self):
        self.lease_info_list = [
            LeaseInfo(lease_renewal_interval_in_secs=1, lease_duration_in_secs=1),
            LeaseInfo(lease_renewal_interval_in_secs=2, lease_duration_in_secs=2),
        ]

        self.instance_info_list = [
            instance_info(app_name="app_1", num=1147),
            instance_info(app_name="app_1", num=1148),
            instance_info(app_name="app_2", num=1149),
        ]
        self.instance_info_list[0].action_type = InstanceInfo.ActionType.ADD
        self.instance_info_list[0].status = InstanceInfo.Status.UP
        self.instance_info_list[0].lease_info = self.lease_info_list[0]

        application_1 = Application("app_1")
        application_1.add_instance(self.instance_info_list[0])
        application_1.add_instance(self.instance_info_list[1])
        application_2 = Application("app_2")
        application_2.add_instance(self.instance_info_list[2])
        self.application_list = [application_1, application_2]

        applications = Applications()
        applications.add_application(application_1)
        applications.add_application(application_2)
        self.applications = applications

    def test_lease_info_model(self):
        lease_info_model = LeaseInfoModel.from_entity(self.lease_info_list[0])

        assert lease_info_model.lease_renewal_interval_in_secs == 1

    def test_instance_info_model(self):
        instance_info_model = InstanceInfoModel.from_entity(self.instance_info_list[0])

        assert instance_info_model.instance_id == "1147"
        assert instance_info_model.lease_info.lease_renewal_interval_in_secs == 1
        assert instance_info_model.action_type == "ADD"
        assert instance_info_model.status == "UP"

    def test_application_model(self):
        application_model = ApplicationModel.from_entity(self.application_list[0])

        assert application_model.name == "app_1"
        assert application_model.instance_info_model_list[0].app_name == "app_1"

    def test_applications_model(self):
        applications_model = ApplicationsModel.from_entity(self.applications)

        assert len(applications_model.application_model_list) == 2
        assert applications_model.application_model_list[0].name == "app_1"
        assert applications_model.application_model_list[0].instance_info_model_list[0].instance_id == "1147"


class TestToEntity:
    def setup_method(self):
        self.lease_info_model_list = [
            lease_info_model_template(lease_renewal_interval_in_secs=1, lease_duration_in_secs=1,),
            lease_info_model_template(lease_renewal_interval_in_secs=30, lease_duration_in_secs=90,),
        ]

        self.instance_info_model_list = [
            instance_info_model_template(
                "instance_1",
                "app_1",
                action_type="ADD",
                port=8787,
                status="UP",
                overridden_status="UNKNOWN",
                lease_info=self.lease_info_model_list[0],
            ),
            instance_info_model_template("instance_2", "app_1", lease_info=self.lease_info_model_list[1]),
        ]

        application_model_1 = ApplicationModel(
            name="app_1", instance_info_model_list=[self.instance_info_model_list[0], self.instance_info_model_list[1]],
        )

        application_model_2 = ApplicationModel(name="app_2", instance_info_model_list=[])

        self.application_model_list = [
            application_model_1,
            application_model_2,
        ]

        self.applications_model = ApplicationsModel(application_model_list=[application_model_1, application_model_2])

    def test_lease_info_model(self):
        lease_info = self.lease_info_model_list[0].to_entity()

        assert 0 == lease_info.registration_timestamp
        assert 1 == lease_info.lease_renewal_interval_in_secs

    def test_instance_info_model(self):
        instance_info_entity = self.instance_info_model_list[0].to_entity()

        assert instance_info_entity.instance_id == "instance_1"
        assert instance_info_entity.ip_address == "127.0.0.1"
        assert instance_info_entity.status == InstanceInfo.Status.UP
        assert instance_info_entity.last_updated_timestamp is None
        assert instance_info_entity.is_unsecure_port_enabled
        assert instance_info_entity.port == 8787
        assert instance_info_entity.action_type == InstanceInfo.ActionType.ADD

    def test_application_model(self):
        application = self.application_model_list[0].to_entity()

        assert application.name == "app_1"
        assert application.size() == 2
        assert application.get_instance_by_id("instance_1").port == 8787

    def test_applications_model(self):
        applications = self.applications_model.to_entity()

        assert 2 == applications.size()
        assert 2 == applications.get_registered_application("app_1").size()
