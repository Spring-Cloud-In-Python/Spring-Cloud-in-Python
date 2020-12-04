# -*- coding: utf-8 -*-

__author__ = "Ricky"
__license__ = "Apache 2.0"
# standard library
from abc import ABC, abstractmethod


class EurekaServerContext(ABC):
    @abstractmethod
    def initialize(self):
        pass

    @abstractmethod
    def shutdown(self):
        pass

    @abstractmethod
    def server_config(self):
        pass

    @abstractmethod
    def peer_eureka_nodes(self):
        pass

    @abstractmethod
    def server_codecs(self):
        pass

    @abstractmethod
    def peer_aware_instance_registry(self):
        pass

    @abstractmethod
    def application_info_manager(self):
        pass
