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

    def encode_application(self, application: Application) -> Dict:
        pass

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

    def decode_application(self, application_dict: Dict) -> Application:
        pass

    def decode_applications(self, applications_dict: Dict) -> Applications:
        pass
