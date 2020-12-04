# -*- coding: utf-8 -*-

__author__ = "Waterball (johnny850807@gmail.com)"
__license__ = "Apache 2.0"


def enable_service_discovery():
    # TODO: implement the bootstrapping
    pass


def enable_service_registry(port=8761):
    # TODO: Fake, should be substituted with the real implementation
    # standard library
    import time

    while True:
        time.sleep(3)
        print("Tick...")  # simulate service' running
