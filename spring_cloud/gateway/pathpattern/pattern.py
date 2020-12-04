# -*- coding: utf-8 -*-
from .elements import PathElement

__author__ = "Waterball (johnny850807@gmail.com)"
__license__ = "Apache 2.0"

__all__ = ["PathPattern", "MatchingContext"]


class PathPattern:
    def __init__(self, path_pattern: str, head_path_element: PathElement):
        self.head_path_element = head_path_element
        self.path_pattern = path_pattern

    def matches(self, path: str):
        pass


class MatchingContext:
    pass
