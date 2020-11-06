# -*- coding: utf-8 -*-
# standard library
from typing import Iterable

__author__ = "Waterball (johnny850807@gmail.com)"
__license__ = "Apache 2.0"


def flat_map(f, xs: Iterable):
    """
    :param f: a mapping function
    :param xs: (Iterable)
    :return: list
    """
    return [item for element in xs for item in f(element)]


def filter_get_first(f, xs: Iterable):
    """
    :param f: a predicate function that returns a boolean
    :param xs: (Iterable)
    :return: the first element matches the predicate
    """
    return next((x for x in xs if f(x)), None)
