# -*- coding: utf-8 -*-
from __future__ import annotations

__author__ = "Daniel1147 (sxn91401@gmail.com)"
__license__ = "Apache 2.0"

# standard library
from typing import List

# pypi/conda library
from pydantic import BaseModel

# scip plugin
from eureka.client.discovery.shared import Applications
from eureka.model.application_model import ApplicationModel


class ApplicationsModel(BaseModel):
    application_model_list: List[ApplicationModel]
    reconciliation_hash_code: str = ""

    @staticmethod
    def from_entity(applications: Applications) -> ApplicationsModel:
        application_model_list = [
            ApplicationModel.from_entity(application) for application in applications.get_registered_applications()
        ]

        return ApplicationsModel(
            application_model_list=application_model_list,
            reconciliation_hash_code=applications.reconciliation_hash_code,
        )

    def to_entity(self) -> Applications:
        applications = Applications()
        for application_model in self.application_model_list:
            application = application_model.to_entity()
            applications.add_application(application)

        applications.reconciliation_hash_code = self.reconciliation_hash_code

        return applications
