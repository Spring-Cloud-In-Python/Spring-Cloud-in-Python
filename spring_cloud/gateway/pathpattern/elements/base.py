# -*- coding: utf-8 -*-
# standard library
from abc import ABC, abstractmethod
from typing import Optional

__author__ = "Waterball (johnny850807@gmail.com)"
__license__ = "Apache 2.0"

__all__ = ["PathElement"]


class PathElement(ABC):
    def __init__(self, pos: int, separator):
        self.pos = pos
        self.separator = separator
        self.next: Optional[PathElement] = None
        self.prev: Optional[PathElement] = None

    @abstractmethod
    def matches(self, path_pos: int, matching_context):
        raise NotImplemented

    @property
    @abstractmethod
    def text(self):
        raise NotImplemented

    def is_no_more_pattern(self) -> bool:
        return self.next is None
