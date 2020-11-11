# -*- coding: utf-8 -*-

__author__ = "Daniel1147 (sxn91401@gmail.com)"
__license__ = "Apache 2.0"

# standard library
import enum
from datetime import datetime


class Lease:
    class Action(enum.Enum):
        REGISTER = "register"
        CANCEL = "cancel"
        RENEW = "renew"

    def __init__(self, holder, duration_in_secs):
        self.durationInSecs = duration_in_secs
        self.holder = holder
        self.registration_timestamp = datetime.now().microsecond

    @property
    def holder(self):
        return self._holder

    @holder.setter
    def holder(self, holder):
        self._holder = holder

    def is_expired(self):
        return False
