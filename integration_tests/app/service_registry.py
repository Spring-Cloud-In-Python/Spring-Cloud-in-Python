# -*- coding: utf-8 -*-
# scip plugin
import spring_cloud.context.bootstrap as spring_cloud_bootstrap

__author__ = "Waterball (johnny850807@gmail.com)"
__license__ = "Apache 2.0"

if __name__ == "__main__":
    # standard library
    import os

    port = int(os.getenv("port"))
    spring_cloud_bootstrap.enable_service_registry(port=port)
