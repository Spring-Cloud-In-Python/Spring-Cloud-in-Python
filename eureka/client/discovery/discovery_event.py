# -*- coding: utf-8 -*-

__author__ = "Haribo (haribo1558599@gmail.com)"
__license__ = "Apache 2.0"

# scip plugin
from eureka.client.discovery.eureka_event import EurekaEvent
from eureka.utils.timestamp import current_timestamp


class DiscoveryEvent(EurekaEvent):
    def __init__(self):
        self._timestamp = current_timestamp()

    @property
    def timestamp(self):
        return self._timestamp
