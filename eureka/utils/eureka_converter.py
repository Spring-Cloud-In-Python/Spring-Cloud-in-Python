# -*- coding: utf-8 -*-

__author__ = "Daniel1147 (sxn91401@gmail.com)"
__license__ = "Apache 2.0"

# standard library
from enum import Enum
from typing import Dict

# scip plugin
from eureka.client.app_info import InstanceInfo, LeaseInfo
from eureka.client.discovery.shared import Application, Applications


class EurekaEncoder:
    def encode_lease_info(self, lease_info: LeaseInfo) -> Dict:
        slots = lease_info.__slots__
        result = {}
        for property_name in slots:
            property_key = property_name[1:]  # skip the beginning "_"

            result[property_key] = getattr(lease_info, property_name)

        return result

    def encode_instance(self, instance_info: InstanceInfo) -> Dict:
        slots = instance_info.__slots__
        result = {}

        property_to_skip = ["_lease_info", "_is_instance_info_dirty"]
        for property_name in slots:
            if property_name in property_to_skip:
                continue

            property_key = property_name[1:]  # skip the beginning "_"

            value = getattr(instance_info, property_name)
            if isinstance(value, Enum):
                value = str(value)

            result[property_key] = value

        result["lease_info"] = self.encode_lease_info(instance_info.lease_info)

        return result

    def encode_application(self, application: Application) -> Dict:
        result = {"name": application.name, "is_dirty": application.is_dirty}
        instance_list = application.get_all_instances_from_local_cache()
        instance_dict_list = []
        for instance in instance_list:
            instance_dict_list.append(self.encode_instance(instance))
        result["instance_dict"] = instance_dict_list

        return result

    def encode_applications(self, applications: Applications) -> Dict:
        result = {"applications": []}

        for application in applications.get_registered_applications():
            result["applications"].append(self.encode_application(application))

        return result


class EurekaDecoder:
    def __init__(self):
        self.instance_info_enum_transform_table = {
            "status": InstanceInfo.Status,
            "overridden_status": InstanceInfo.Status,
            "action_type": InstanceInfo.ActionType,
        }

    def decode_lease_info(self, lease_dict: Dict) -> LeaseInfo:
        lease = LeaseInfo(**lease_dict)

        return lease

    def decode_instance(self, instance_dict: Dict) -> InstanceInfo:
        lease = self.decode_lease_info(instance_dict["lease_info"])
        instance_dict["lease_info"] = lease

        for property_name, enum_type in self.instance_info_enum_transform_table.items():
            property_value = instance_dict[property_name]  # e.g. "Status.UP", None

            if property_value is None:
                continue

            property_value = property_value.split(".")[-1]  # e.g. "UP"
            instance_dict[property_name] = enum_type(property_value)

        instance_info = InstanceInfo(**instance_dict)

        return instance_info

    def decode_application(self, application_dict: Dict) -> Application:
        application = Application(application_dict["name"])
        instance_dict_list = application_dict["instance_dict"]
        for instance_dict in instance_dict_list:
            instance = self.decode_instance(instance_dict)
            application.add_instance(instance)

        application._is_dirty = application_dict["is_dirty"]  # overwrite this protected value since there is no setter

        return application

    def decode_applications(self, applications_dict: Dict) -> Applications:
        applications = Applications()
        for application_dict in applications_dict["applications"]:
            application = self.decode_application(application_dict)
            applications.add_application(application)

        return applications
