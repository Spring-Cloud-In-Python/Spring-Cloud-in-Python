# -*- coding: utf-8 -*-
# scip plugin
from commons.client.service_instance import StaticServiceInstance

__author__ = "Waterball (johnny850807@gmail.com)"
__license__ = "Apache 2.0"


SERVICE_ID = "serviceId"
INSTANCES = [StaticServiceInstance("uri", SERVICE_ID, instance_id) for instance_id in ["1", "2", "3"]]
