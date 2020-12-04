# -*- coding: utf-8 -*-
# standard library
from abc import ABC
from typing import List, Optional

# scip plugin
import spring_cloud.utils.validate as validate

from .elements import PathElement

__author__ = "Waterball (johnny850807@gmail.com)"
__license__ = "Apache 2.0"

__all__ = ["PathPattern", "MatchingContext", "PathContainer"]


class PathContainer:
    @staticmethod
    def from_path(path: str, separator="/"):
        segments = path.split(separator)[1:]  # skip the first separator
        elements = []
        for segment in segments:
            elements.append(PathContainer.Separator(separator))
            elements.append(PathContainer.PathSegment(segment))
        return PathContainer(elements)

    def __init__(self, elements: List):
        self.path_elements: List[PathContainer.Element] = elements

    def path_element_value(self, pos):
        return self.path_elements[pos].text

    class Element(ABC):
        def __init__(self, text):
            self.text = text

    class PathSegment(Element):
        pass

    class Separator(Element):
        pass

    def is_empty(self):
        return len(self.path_elements) == 0


class MatchingContext:
    def __init__(self, path_container: PathContainer, path_pattern):
        self.path_pattern = path_pattern
        self.path_container = path_container
        self.path_elements = path_container.path_elements

    @property
    def path_length(self):
        return len(self.path_container.path_elements)

    def get_element(self, index):
        return self.path_elements[index]

    def is_separator(self, index):
        return isinstance(self.get_element(index), PathContainer.Separator)


class PathPattern:
    def __init__(self, path_pattern: str, separator, head_path_element: PathElement):
        self.head = head_path_element
        self.separator = separator
        self.path_pattern = path_pattern

    def matches(self, path: str = None, path_container: Optional[PathContainer] = None):
        if path_container:
            return self.__matches_path_container(path_container)
        else:
            validate.not_none(path)
            return self.matches(path_container=PathContainer.from_path(path, self.separator))

    def __matches_path_container(self, path_container: PathContainer):
        if not self.head:
            return path_container.is_empty()
        elif path_container.is_empty():
            return False
        matching_context = MatchingContext(path_container, self)
        return self.head.matches(0, matching_context)
