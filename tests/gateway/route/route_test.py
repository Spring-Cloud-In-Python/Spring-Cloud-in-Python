# -*- coding: utf-8 -*-

__author__ = "Chaoyuuu (chaoyu2330@gmail.com)"
__license__ = "Apache 2.0"

# scip plugin
from spring_cloud.gateway.handler.predicate import TRUE
from spring_cloud.gateway.route import Route


class TestRoute:
    def test_init_Route_when_build(self):
        builder = Route.Builder()
        route = builder.set_uri("http://a_Cat").set_predicate(TRUE).set_route_id(1).build()
        assert route.uri == "http://a_Cat"
        assert route.predicate
        assert route.route_id == 1
