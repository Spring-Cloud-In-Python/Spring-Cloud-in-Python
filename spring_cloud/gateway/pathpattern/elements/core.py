# -*- coding: utf-8 -*-
"""
The expression elements
"""
from ..pattern import MatchingContext, PathContainer
from .base import PathElement

__author__ = "Waterball (johnny850807@gmail.com)"
__license__ = "Apache 2.0"

__all__ = ["LiteralPathElement", "SeparatorPathElement", "WildcardTheRestPathElement"]


class LiteralPathElement(PathElement):
    def __init__(self, pos: int, literal_text: str, separator):
        super().__init__(pos, separator)
        self.literal_text = literal_text

    def matches(self, path_index: int, context: MatchingContext) -> bool:
        if path_index >= context.path_length:
            return False
        element = context.get_element(path_index)
        if not isinstance(element, PathContainer.PathSegment):
            return False
        match = self.literal_text == element.text
        if not match:
            return False
        if self.has_no_next_element():
            return path_index + 1 == context.path_length
        else:
            return self.next.matches(path_index + 1, context)

    @property
    def text(self) -> str:
        return self.literal_text


class SeparatorPathElement(PathElement):
    def __init__(self, pos: int, separator):
        super().__init__(pos, separator)

    def matches(self, path_index: int, context: MatchingContext) -> bool:
        if path_index < context.path_length and context.is_separator(path_index):
            if self.has_no_next_element():
                return path_index + 1 == context.path_length
            else:
                return self.next.matches(path_index + 1, context)
        return False

    @property
    def text(self) -> str:
        return self.separator


# TODO
class WildcardTheRestPathElement(PathElement):
    def matches(self, path_index: int, context: MatchingContext) -> bool:
        pass

    @property
    def text(self) -> str:
        pass
