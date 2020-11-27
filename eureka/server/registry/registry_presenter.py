# -*- coding: utf-8 -*-
from __future__ import annotations

__author__ = "Daniel1147 (sxn91401@gmail.com)"
__license__ = "Apache 2.0"


# standard library
import json
from typing import TYPE_CHECKING

# scip plugin
from eureka.utils.eureka_converter import EurekaEncoder

if TYPE_CHECKING:
    # scip plugin
    from eureka.server.registry.instance_registry import InstanceRegistry


class RegistryPresenter:
    def __init__(self, registry: InstanceRegistry):
        self.registry = registry
        self.encoder = EurekaEncoder()

    def query_application(self, application_name: str) -> str:
        application = self.registry.get_application(application_name)
        application_dict = self.encoder.encode_application(application)
        response = json.dumps(application_dict)

        return response

    def query_applications(self) -> str:
        applications = self.registry.get_applications()
        applications_dict = self.encoder.encode_applications(applications)
        response = json.dumps(applications_dict)

        return response
