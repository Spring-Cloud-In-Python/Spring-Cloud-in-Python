# -*- coding: utf-8 -*-
# scip plugin
import spring_cloud.context.bootstrap as spring_cloud_bootstrap

__author__ = "Waterball (johnny850807@gmail.com)"
__license__ = "Apache 2.0"

if __name__ == "__main__":
    spring_cloud_bootstrap.enable_service_registry(port=10000)
