# -*- coding: utf-8 -*-
"""
The expression elements
"""
from ..pattern import MatchingContext
from .base import PathElement

__author__ = "Waterball (johnny850807@gmail.com)"
__license__ = "Apache 2.0"

__all__ = ["LiteralPathElement", "SeparatorPathElement", "WildcardTheRestPathElement"]


class LiteralPathElement(PathElement):
    def __init__(self, pos: int, literal_text: str, separator):
        super().__init__(pos, separator)
        self.literal_text = literal_text

    def matches(self, path_pos: int, matching_context):
        pass

    @property
    def text(self):
        return self.literal_text


class SeparatorPathElement(PathElement):
    def __init__(self, pos: int, separator):
        super().__init__(pos, separator)

    def matches(self, path_pos: int, context: MatchingContext):
        pass

    @property
    def text(self):
        return self.separator


class WildcardTheRestPathElement(PathElement):
    def matches(self, path_pos: int, context: MatchingContext):
        pass

    @property
    def text(self):
        pass
