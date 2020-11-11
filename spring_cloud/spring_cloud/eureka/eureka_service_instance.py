# -*- coding: utf-8 -*-

__author__ = "Ricky"
__license__ = "Apache 2.0"

# scip plugin
from spring_cloud.spring_cloud.eureka.instanceinfo import InstanceInfo


class EurekaServiceInstance:
    def __init__(self):
        self.instance_info = InstanceInfo()

    def get_instance_info(self):
        return self.instance_info
