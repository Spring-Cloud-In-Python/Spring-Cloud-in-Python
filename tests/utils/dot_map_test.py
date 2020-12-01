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


def test_when_init_with_none_key_val_pair_should_raise():
    with pytest.raises(TypeError):
        dot_map = DotMap("MJ is awesome")


def test_add_key_val_pair_and_access():
    dot_map = DotMap()
    dot_map.mj = "MJ is awesome"

    assert dot_map.mj == "MJ is awesome"


def test_when_access_nonexistent_key_should_raise():
    dot_map = DotMap()
    with pytest.raises(AttributeError):
        val = dot_map.mj


def test_nested_dot_map():
    dot_map = DotMap()
    dot_map.mj = DotMap(face="handsome")
    assert dot_map.mj.face == "handsome"
