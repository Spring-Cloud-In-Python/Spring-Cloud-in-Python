# standard library
from functools import reduce

__author__ = "Waterball (johnny850807@gmail.com)"
__license__ = "Apache 2.0"


def flat_map(f, xs):
    results = []
    for element in xs:
        results += f(element)
    return results


def filter_get_first(f, the_list):
    return [x for x in the_list if f(x)][0]
