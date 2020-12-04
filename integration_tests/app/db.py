# -*- coding: utf-8 -*-
"""
In-Memory data access module.
"""
# standard library
from typing import Optional

from .entities import Message, User
from .errors import NotFoundError

__author__ = "Waterball (johnny850807@gmail.com)"
__license__ = "Apache 2.0"


class Users:
    db = {}

    @staticmethod
    def find_by_id(id_: int) -> Optional[User]:
        return Users.db[id_]

    @staticmethod
    def find_by_account_and_password(account: str, password: str):
        result = [user for user in Users.db.values() if user.account == account and user.password == password]
        if len(result) == 0:
            raise NotFoundError()
        return result[0]

    @staticmethod
    def save(user: User):
        user.id = len(Users.db.keys())
        Users.db[user.id] = user
        return user


class Messages:
    db = []

    @staticmethod
    def find_all():
        return list(Messages.db)

    @staticmethod
    def save(message: Message):
        message.id = len(Messages.db)
        Messages.db.append(message)
        return message
