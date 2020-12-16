# -*- coding: utf-8 -*-

__author__ = "Haribo (haribo1558599@gmail.com)"
__license__ = "Apache 2.0"

# standard library
from typing import Dict


class EurekaHttpResponse:
    __slots__ = ("_status_code", "_entity", "_headers", "_location")

    LOCATION = "Location"

    def __init__(self, headers: Dict[str, str], status_code: int = 200, entity=None):
        self._status_code = status_code
        self._entity = entity
        self._headers = headers
        self._location = headers.get(self.LOCATION, "")

    @property
    def status_code(self) -> int:
        return self._status_code

    @property
    def entity(self):
        return self._entity

    @entity.setter
    def entity(self, entity):
        self._entity = entity

    @property
    def headers(self) -> Dict[str, str]:
        return self._headers

    @property
    def location(self) -> str:
        return self._location
