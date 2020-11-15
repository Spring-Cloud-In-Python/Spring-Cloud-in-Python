# -*- coding: utf-8 -*-

__author__ = "MJ (tsngmj@gmail.com)"
__license__ = "Apache 2.0"

# scip plugin
from ribbon.calculator.calculator import Calculator


def test_plus():
    calculator = Calculator()
    value = calculator.eval("3 + 3")
    assert value == 6
