# -*- coding: utf-8 -*-
from __future__ import annotations

__author__ = "Daniel1147 (sxn91401@gmail.com)"
__license__ = "Apache 2.0"


# standard library
import json
from typing import TYPE_CHECKING, Optional

# scip plugin
from eureka.model.application_model import ApplicationModel
from eureka.model.applications_model import ApplicationsModel

if TYPE_CHECKING:
    # scip plugin
    from eureka.server.registry.instance_registry import InstanceRegistry


class RegistryPresenter:
    def __init__(self, registry: InstanceRegistry):
        self.registry = registry

    def query_application(self, application_name: str) -> Optional[ApplicationModel]:
        application = self.registry.get_application(application_name)
        if application is None:
            return None

        application_model = ApplicationModel.from_entity(application)

        return application_model

    def query_applications(self) -> ApplicationsModel:
        applications = self.registry.get_applications()
        applications_model = ApplicationsModel.from_entity(applications)

        return applications_model
