# -*- coding: utf-8 -*-
# scip plugin
from spring_cloud.commons.utils.list_utils import not_none_nor_empty

__author__ = "Waterball (johnny850807@gmail.com)"
__license__ = "Apache 2.0"


def test_not_none_nor_empty():
    assert not_none_nor_empty([1])
    assert not not_none_nor_empty([])
