# -*- coding: utf-8 -*-
"""
Parser that applies interpreter pattern.

Reference: https://github.com/spring-projects/spring-framework/blob/8ac39a50feda71194e33a456c0f8207169a5a3a9/spring-web/src/main/java/org/springframework/web/util/pattern/InternalPathPatternParser.java#L300
"""
# scip plugin
from spring_cloud.utils.validate import not_none

from .elements import LiteralPathElement, PathElement, SeparatorPathElement
from .pattern import PathPattern

__author__ = "Waterball (johnny850807@gmail.com)"
__license__ = "Apache 2.0"

__all__ = ["PathPatternParser"]

SEPARATOR = "/"


class PathPatternParser:
    @staticmethod
    def parse(path_pattern: str) -> PathPattern:
        return InternalPathPatternParser().parse(path_pattern)


class InternalPathPatternParser:
    """
    The algorithm that parses tha pattern into the abstract syntax tree (though in our case,
        it's barely a linked-list rather than a tree)
    """

    def __init__(self):
        self.path_pattern: str = None
        self.pos: int = 0
        self.separator = SEPARATOR
        self.path_element_start = -1
        self.head_path_element: PathElement = None
        self.current_path_element: PathElement = None

    def parse(self, path_pattern: str) -> PathPattern:
        self.path_pattern = not_none(path_pattern)
        self.__reset_path_element_state()

        # interpretation
        while self.pos < len(self.path_pattern):
            self.__parse_next_character()

        return PathPattern(path_pattern, self.head_path_element)

    def __reset_path_element_state(self):
        self.path_element_start = -1

    def __parse_next_character(self):
        ch = self.path_pattern[self.pos]

        if ch == self.separator:
            if self.path_element_start != -1:
                self.__push_path_element(
                    LiteralPathElement(self.path_element_start, self.__extract_path_element_text(), self.separator)
                )
            self.__push_path_element(SeparatorPathElement(self.pos, self.separator))
        else:
            if self.path_element_start == -1:
                self.path_element_start = self.pos

        self.pos += 1

    def __push_path_element(self, new_path_element: PathElement):
        if not self.head_path_element:
            self.head_path_element = new_path_element
            self.current_path_element = new_path_element
        elif self.current_path_element:
            self.current_path_element.next = new_path_element
            new_path_element.prev = self.current_path_element
            self.current_path_element = new_path_element

        self.__reset_path_element_state()

    def __extract_path_element_text(self):
        return self.path_pattern[self.path_element_start : self.pos]
