# -*- coding: utf-8 -*-
from __future__ import annotations

# standard library
from abc import ABC

__author__ = "Chaoyuuu (chaoyu2330@gmail.com)"
__license__ = "Apache 2.0"

# scip plugin
from spring_cloud.gateway.handler.predicate.predicate import Predicate


class GatewayPredicate(ABC, Predicate):
    pass
