# -*- coding: utf-8 -*-

__author__ = "Daniel1147 (sxn91401@gmail.com)"
__license__ = "Apache 2.0"

# standard library
from typing import Dict

# scip plugin
from eureka.client.app_info import InstanceInfo, LeaseInfo
from eureka.client.discovery.shared import Application, Applications


class Encoder:
    @staticmethod
    def encode_lease_info(lease: LeaseInfo) -> Dict:
        slots = lease.__slots__
        result = {}
        for property_name in slots:
            property_name = property_name[1:]  # skip the beginning "_"

            result[property_name] = getattr(lease, property_name)

        return result

    @staticmethod
    def encode_instance(info: InstanceInfo) -> Dict:
        slots = info.__slots__
        result = {}
        for property_name in slots:
            if property_name == "_lease_info":
                # do LeaseInfo in another way
                continue

            property_name = property_name[1:]  # skip the beginning "_"

            value = getattr(info, property_name)
            if isinstance(value, InstanceInfo.Status):
                value = str(value)

            result[property_name] = value

        result["lease_info"] = Encoder.encode_lease_info(info.lease_info)

        return result

    @staticmethod
    def encode_application(application: Application) -> Dict:
        result = {"name": application.name, "is_dirty": application.is_dirty}
        instance_list = application.get_all_instances_from_local_cache()
        instance_dict_list = []
        for instance in instance_list:
            instance_dict_list.append(Encoder.encode_instance(instance))
        result["instance_dict"] = instance_dict_list

        return result

    def encode_applications(self, applications: Applications) -> Dict:
        pass


class Decoder:
    @staticmethod
    def decode_lease_info(lease_dict: Dict) -> LeaseInfo:
        lease = LeaseInfo(**lease_dict)

        return lease

    @staticmethod
    def decode_instance(instance_dict: Dict) -> InstanceInfo:
        lease = Decoder.decode_lease_info(instance_dict["lease_info"])
        instance_dict["lease_info"] = lease

        status_property = ["status", "overridden_status"]
        for property_name in status_property:
            property_value = instance_dict[property_name]  # e.g. "Status.UP"
            property_value = property_value.split(".")[-1]  # e.g. "UP"
            instance_dict[property_name] = InstanceInfo.Status(property_value)

        instance_info = InstanceInfo(**instance_dict)

        return instance_info

    @staticmethod
    def decode_application(application_dict: Dict) -> Application:
        application = Application(application_dict["name"])
        instance_dict_list = application_dict["instance_dict"]
        for instance_dict in instance_dict_list:
            instance = Decoder.decode_instance(instance_dict)
            application.add_instance(instance)

        application._is_dirty = application_dict["is_dirty"]  # overwrite this protected value since there is no setter

        return application

    def decode_applications(self, applications_dict: Dict) -> Applications:
        pass
