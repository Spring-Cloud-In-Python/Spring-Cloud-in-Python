# -*- coding: utf-8 -*-

__author__ = "MJ (tsngmj@gmail.com)"
__license__ = "Apache 2.0"

# pypi/conda library
import pytest

# scip plugin
from spring_cloud.utils.dot_map import DotMap


def test_generate_an_empty_dot_map():
    dot_map = DotMap()
    assert dot_map == {}


def test_generate_an_dot_map_with_given_none_map_data():
    with pytest.raises(TypeError):
        dot_map = DotMap("MJ is awesome")


def test_add_a_none_pair_data_into_dot_map():
    dot_map = DotMap()
    dot_map.mj = "MJ is awesome"

    assert dot_map.mj == "MJ is awesome"


def test_get_value_with_given_unexist_key():
    dot_map = DotMap()
    with pytest.raises(AttributeError):
        val = dot_map.mj
