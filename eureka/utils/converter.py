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

    def encode_instance(self, info: InstanceInfo) -> Dict:
        pass

    def encode_application(self, application: Application) -> Dict:
        pass

    def encode_applications(self, applications: Applications) -> Dict:
        pass


class Decoder:
    @staticmethod
    def decode_lease_info(lease_dict: Dict) -> LeaseInfo:
        lease = LeaseInfo(**lease_dict)

        return lease

    def decode_instance(self, instance_dict: Dict) -> InstanceInfo:
        pass

    def decode_application(self, application_dict: Dict) -> Application:
        pass

    def decode_applications(self, applications_dict: Dict) -> Applications:
        pass
