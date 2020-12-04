# -*- coding: utf-8 -*-

__author__ = "Ricky"
__license__ = "Apache 2.0"
# scip plugin
from eureka.core.eureka_server_context import EurekaServerContext


class EurekaServerContextHolder:
    def __init__(self, server_context: EurekaServerContext):
        self.__server_context = server_context
        self.__holder = None

    @property
    def server_context(self):
        return self.__server_context

    def initialize(self, server_context):
        self.__holder = EurekaServerContextHolder(server_context)

    def get_instance(self):
        return self.__holder
