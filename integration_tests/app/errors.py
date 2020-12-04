# -*- coding: utf-8 -*-
# pypi/conda library
from fastapi import HTTPException

__author__ = "Waterball (johnny850807@gmail.com)"
__license__ = "Apache 2.0"


class NotFoundError(HTTPException):
    def __init__(self):
        super().__init__(status_code=404)
