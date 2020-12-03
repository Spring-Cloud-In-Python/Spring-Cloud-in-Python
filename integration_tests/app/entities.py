# -*- coding: utf-8 -*-

__author__ = "Waterball (johnny850807@gmail.com)"
__license__ = "Apache 2.0"

# standard library
# -*- coding: utf-8 -*-
from typing import Optional


class User:
    def __init__(self, name, account, password, id_: Optional[str] = None):
        self.id = id_
        self.name = name
        self.account = account
        self.password = password


class Message:
    def __init__(self, poster_id: int, content: str, id_: Optional[int] = None):
        self.id = id_
        self.poster_id = poster_id
        self.content = content
