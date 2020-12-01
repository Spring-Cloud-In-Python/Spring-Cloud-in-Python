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
        obj = {"name": application.name}
        instance_info_list = application.get_all_instances_from_local_cache()
        instance_info_model_list = []
        for instance in instance_info_list:
            instance_info_model_list.append(InstanceInfoModel.from_entity(instance))
        obj["instance_info_model_list"] = instance_info_model_list

        return ApplicationModel(**obj)

    def to_entity(self) -> LeaseInfo:
        application = Application(self.name)
        for instance_info_model in self.instance_info_model_list:
            instance = instance_info_model.to_entity()
            application.add_instance(instance)

        return application
