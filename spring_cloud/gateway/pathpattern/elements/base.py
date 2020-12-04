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
    def matches(self, path_index: int, matching_context) -> bool:
        raise NotImplemented

    @property
    @abstractmethod
    def text(self) -> str:
        raise NotImplemented

    def has_no_next_element(self) -> bool:
        return self.next is None
