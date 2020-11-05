# standard library
from functools import reduce

__author__ = "Waterball (johnny850807@gmail.com)"
__license__ = "Apache 2.0"


def flat_map(f, xs):
    return reduce(lambda a, b: a + b, map(f, xs))


def filter_get_first(f, the_list):
    return next(filter(f, the_list), None)
