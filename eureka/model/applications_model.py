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

    @staticmethod
    def from_entity(applications: Applications) -> ApplicationsModel:
        application_model_list = []

        for application in applications.get_registered_applications():
            application_model_list.append(ApplicationModel.from_entity(application))

        return ApplicationsModel(application_model_list=application_model_list)

    def to_entity(self) -> Applications:
        applications = Applications()
        for application_model in self.application_model_list:
            application = application_model.to_entity()
            applications.add_application(application)

        return applications
