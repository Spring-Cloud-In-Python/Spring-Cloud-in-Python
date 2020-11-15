# -*- coding: utf-8 -*-
# scip plugin
from spring_cloud.commons.exceptions.primitive import NoneTypeError

__author__ = "Waterball (johnny850807@gmail.com)"
__license__ = "Apache 2.0"


def not_none(obj):
    if obj:
        return obj
    raise NoneTypeError


def is_instance_of(obj, the_type):
    if isinstance(obj, the_type):
        return obj
    raise TypeError()
