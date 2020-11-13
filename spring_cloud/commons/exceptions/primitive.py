# -*- coding: utf-8 -*-
"""
All primitive exceptions are included here
"""

__author__ = "Waterball (johnny850807@gmail.com)"
__license__ = "Apache 2.0"


class NoneTypeError(Exception):
    def __init__(self, message):
        self.message = message
