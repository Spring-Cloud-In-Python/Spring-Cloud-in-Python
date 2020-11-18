# -*- coding: utf-8 -*-

__author__ = "Ricky"
__license__ = "Apache 2.0"


class InstanceInfo:
    def __init__(self, ID, app_name):
        self.description = "this is for my test"
        self.id = ID
        self.app_name = app_name
        self.host_name = "host_name"
        self.secure_port = "secure_port"
        self.port = "port"
        self.port_enabled = "port_enabled"
        self.isSecurePortEnabled = False
        self.isUnSecurePortEnabled = True

    def get_id(self):
        return self.id

    def get_app_name(self):
        return self.app_name

    def get_host_name(self):
        return self.host_name

    def get_secure_port(self):
        return self.secure_port

    def get_port(self):
        return self.port

    def is_port_enabled(self, string) -> bool:
        if string == "SECURE":
            return self.isSecurePortEnabled
        return self.isUnSecurePortEnabled
