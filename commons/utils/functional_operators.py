# -*- coding: utf-8 -*-

__author__ = "Waterball (johnny850807@gmail.com)"
__license__ = "Apache 2.0"


def flat_map(f, xs):
    """
    :param f: a mapping function
    :param xs: (Iterable)
    :return: list
    """
    results = []
    for element in xs:
        results += f(element)
    return results


def filter_get_first(f, xs):
    """
    :param f: a mapping function
    :param xs: (Iterable)
    :return: an element
    """
    return [x for x in xs if f(x)][0]
