# -*- coding: utf-8 -*-
"""
All primitive exceptions are included here
"""

__author__ = "Waterball (johnny850807@gmail.com)"
__license__ = "Apache 2.0"


class NoneTypeError(Exception):
    @staticmethod
    def raise_if_none(obj):
        if obj is None:
            raise NoneTypeError

    def __init__(self, message):
        self.message = message


def raise_if_type_not_match(obj, the_type):
    if not isinstance(obj, the_type):
        raise TypeError()
