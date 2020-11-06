# -*- coding: utf-8 -*-

__author__ = "Waterball (johnny850807@gmail.com)"
__license__ = "Apache 2.0"


def not_none_nor_empty(the_list):
    """
    :param the_list: a list
    :return: true if the list is neither none nor empty
    """
    assert not the_list or isinstance(the_list, list)
    return the_list is not None and len(the_list) != 0
