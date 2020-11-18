# -*- coding: utf-8 -*-

__author__ = "Waterball (johnny850807@gmail.com)"
__license__ = "Apache 2.0"


def not_none_nor_empty(the_list: list):
    """
    :return: true if the list is neither none nor empty
    """
    return isinstance(the_list, list) and the_list
