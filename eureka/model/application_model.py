# -*- coding: utf-8 -*-
from __future__ import annotations

__author__ = "Daniel1147 (sxn91401@gmail.com)"
__license__ = "Apache 2.0"

# standard library
from typing import List

# pypi/conda library
from pydantic import BaseModel

# scip plugin
from eureka.client.app_info import LeaseInfo
from eureka.client.discovery.shared import Application
from eureka.model.instance_info_model import InstanceInfoModel


class ApplicationModel(BaseModel):
    name: str
    instance_info_model_list: List[InstanceInfoModel]

    @staticmethod
    def from_entity(application: Application) -> ApplicationModel:
        instance_info_model_list = [
            InstanceInfoModel.from_entity(instance_info)
            for instance_info in application.get_all_instances_from_local_cache()
        ]

        return ApplicationModel(name=application.name, instance_info_model_list=instance_info_model_list)

    def to_entity(self) -> Application:
        application = Application(self.name)
        for instance_info_model in self.instance_info_model_list:
            instance = instance_info_model.to_entity()
            application.add_instance(instance)

        return application
